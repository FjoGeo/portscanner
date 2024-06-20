import unittest
import socket
import errno
from unittest.mock import patch, MagicMock
from myPortScanner import PortScanner


class TestPortScanner(unittest.TestCase):

    @patch('myPortScanner.socket.socket')
    def testConnectOpenPort(self, mockSocket):
        # Mock the socket connection to simulate an open port
        mockSocketInstance = mockSocket.return_value
        mockSocketInstance.connect.return_value = None 

        scanner = PortScanner("127.0.0.1", "80", 1)
        status = scanner.connect("127.0.0.1", 80)

        self.assertEqual(status, "Open")

    
    @patch('myPortScanner.socket.socket')
    def testConnectClosedPort(self, mockSocket):
        # Mock the socket connection to simulate an closed port
        mockSocketInstance = mockSocket.return_value
        mockSocketInstance.connect.side_effect = socket.error(errno.ECONNREFUSED, "Connection refused") 

        scanner = PortScanner("127.0.0.1", "81", 1)
        status = scanner.connect("127.0.0.1", 81)

        self.assertEqual(status, "Closed")


    @patch('myPortScanner.socket.socket')
    def testConnectFilteredPort(self, mockSocket):
        # Mock the socket connection to simulate an closed port
        mockSocketInstance = mockSocket.return_value
        mockSocketInstance.connect.side_effect = socket.timeout

        scanner = PortScanner("127.0.0.1", "82", 1)
        status = scanner.connect("127.0.0.1", 82)

        self.assertEqual(status, "Filtered")


    def testQueue(self):
        scanner = PortScanner("127.0.0.1", "10-12", 1)
        ports = list(scanner.ports)
        self.assertEqual(ports, [10,11,12])


    @patch.object(PortScanner, 'connect', return_value="Open")
    def testStartThreading(self, mockConnect):
        scanner = PortScanner("127.0.0.1", "80-82", 3)
        
        scanner.start_threading()
        
        self.assertEqual(scanner.results[80], "Open")
        self.assertEqual(scanner.results[81], "Open")
        self.assertEqual(scanner.results[82], "Open")

if __name__ == "__main__":
    unittest.main()