from myPortScanner import PortScanner
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Port scanner for basic TCP connect scans.")
    parser.add_argument("target", help="IP or hostname that will be scanned.")
    parser.add_argument("-p", default="1-1024", help="Port range (default 1-1024).")
    parser.add_argument("-t", type=int, default=10, help="Number of threads (default 10).")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    target = args.target
    ports = args.p
    threads = args.t

    scanner = PortScanner(target, ports, threads)
    scanner.print_results()