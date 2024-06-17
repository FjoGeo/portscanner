import argparse, socket, errno, threading, queue


# initialize arguments
parser = argparse.ArgumentParser(description="Port scanner for basic TCP connect scans.")
parser.add_argument("Target", help="ip or hostname that will be scanned.")
parser.add_argument("-p", help="port range (default 1-1024).")
parser.add_argument("-t", type=int, help="number of threads (default 10).")
args = parser.parse_args()


# set scan parameters
def initializeArguments(target, ports:str = "1-1024", threads:int = 10):

    scanTarget = target

    if ports and "-" in ports: # port range
        [minPort, maxPort] = [int(i) for i in ports.split("-")]
        scanPorts = range(minPort, maxPort+1)
    elif ports: # 2+ ports separated by a comma
        scanPorts = [int(i) for i in ports.split(",")]

    if threads:
        scanThreads = threads 

    return scanTarget, scanPorts, scanThreads


target, ports, threads = initializeArguments(args.Target, args.p, args.t)


# parameter
results = {} # dictionary where each thread will store the results of the ports it has scanned
lock = threading.Lock() # a synchronization primitive that prevents state from being modified or accessed by multiple threads of execution at once
q = queue.Queue()


def connect(ip, port) -> str:
    
    status = ""

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        connection = s.connect((ip, port))
        status = "Open"
        s.close()

    except socket.timeout:
        status = "Filtered"

    except socket.error as e:
        if e.errno == errno.ECONNREFUSED:
            status = "Closed"
        else:
            raise e

    return status


def worker():
    while not q.empty():
        (ip,port) = q.get()
        status = connect(ip, port)
        lock.acquire()
        results[ports] = status
        lock.release()
        q.task_done()


for port in ports:
    q.put((target, port))

for i in range(threads):
    t = threading.Thread(target=worker)
    t.start()

print(f"Started a scan of {target} \n {"-" * 10}")
q.join()


for port in ports:
    print(f"Port {str(port)} is {results[port]}")