import socket
import errno
import threading
import queue
import logging


class PortScanner:
    def __init__(self, target, ports: str, threads: int, udp:bool, verbose:bool):
        self.target = target
        self.threads = threads
        self.results = {}
        self.lock = threading.Lock()
        self.q = queue.Queue()
        self.udp = udp
        self.verbose = verbose

        if ports and "-" in ports:
            min_port, max_port = [int(i) for i in ports.split("-")]
            self.ports = range(min_port, max_port + 1)
        elif ports:
            self.ports = [int(i) for i in ports.split(",")]
        else:
            self.ports = range(1, 1025)  # default port range

        logging.basicConfig(filename="port_scan.log", level=logging.INFO)
        self.queue_target_ports()
        self.start_threading()


    def connect(self, port): # TCP scannning
        try:
            s = socket.socket(socket.AF_INET, # IPv4 address
                                socket.SOCK_STREAM) # TCP
            s.settimeout(5)
            s.connect((self.target, port))
            s.close()
            return "Open"
        except socket.timeout:
            s.close()
            return "Filtered"
        except socket.error as e:
            s.close()
            if e.errno == errno.ECONNREFUSED:
                return "Closed"
            else:
                s.close()
                return "Error"

    
    def connect_udp(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.sendto(b"", (self.target, port))
            s.recvfrom(1024)
            s.close()
            return "Open"
        except socket.timeout:
            s.close()
            return "Filtered"
        except socket.error:
            s.close()
            return "Closed"


    def queue_target_ports(self):
        for port in self.ports:
            self.q.put(port)

    def worker(self):
        while not self.q.empty():
            port = self.q.get()
            if self.udp:
                status = self.connect_udp(port)
            else:
                status = self.connect(port)
            with self.lock:
                self.results[port] = status
            self.q.task_done()
            if self.verbose:
                print(f"Scanned port {port}: {status}")

    def start_threading(self):
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.start()
        self.q.join()

    def print_results(self):
        for port in sorted(self.results):
            print(f"Port {port} is {self.results[port]}")


    def log_results(self):
        for port, status in self.results.items():
            logging.info(f"Port {port}: {status}")