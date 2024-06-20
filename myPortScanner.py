import socket
import errno
import threading
import queue


class PortScanner:
    def __init__(self, target, ports: str, threads: int):
        self.target = target
        self.threads = threads
        self.results = {}
        self.lock = threading.Lock()
        self.q = queue.Queue()

        if ports and "-" in ports:
            min_port, max_port = [int(i) for i in ports.split("-")]
            self.ports = range(min_port, max_port + 1)
        elif ports:
            self.ports = [int(i) for i in ports.split(",")]
        else:
            self.ports = range(1, 1025)  # default port range

        self.queue_target_ports()
        self.start_threading()

    def connect(self, target, port):
        try:
            s = socket.socket(socket.AF_INET, # IPv4 address
                                socket.SOCK_STREAM) # TCP
            s.settimeout(5)
            s.connect((target, port))
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

    def queue_target_ports(self):
        for port in self.ports:
            self.q.put(port)

    def worker(self):
        while not self.q.empty():
            port = self.q.get()
            status = self.connect(self.target, port)
            with self.lock:
                self.results[port] = status
            self.q.task_done()

    def start_threading(self):
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.start()
        self.q.join()

    def print_results(self):
        for port in sorted(self.results):
            print(f"Port {port} is {self.results[port]}")