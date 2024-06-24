from myPortScanner import PortScanner
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Port scanner for basic TCP connect scans.")
    parser.add_argument("-target", help="IP or hostname that will be scanned.")
    parser.add_argument("-p", default="1-1024", help="Port range (default 1-1024).")
    parser.add_argument("-t", type=int, default=10, help="Number of threads (default 10).")
    parser.add_argument("-u", default=False, help="Enable UDP scanning.")
    parser.add_argument("-v", default=False, help="Enable verbose output")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    target = args.target
    ports = args.p if args.p else "1-1024"
    threads = args.t if args.t else 10
    udp = args.u
    verbose = args.v

    scanner = PortScanner(target, ports, threads, udp, verbose)
    scanner.print_results()