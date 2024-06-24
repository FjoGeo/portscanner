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

        scanner = PortScanner("127.0.0.1", "80", 1, False, False)
        status = scanner.connect(80)

        self.assertEqual(status, "Open")

    
    @patch('myPortScanner.socket.socket')
    def testConnectClosedPort(self, mockSocket):
        # Mock the socket connection to simulate an closed port
        mockSocketInstance = mockSocket.return_value
        mockSocketInstance.connect.side_effect = socket.error(errno.ECONNREFUSED, "Connection refused") 

        scanner = PortScanner("127.0.0.1", "81", 1, False, False)
        status = scanner.connect(81)

        self.assertEqual(status, "Closed")


    @patch('myPortScanner.socket.socket')
    def testConnectFilteredPort(self, mockSocket):
        # Mock the socket connection to simulate an closed port
        mockSocketInstance = mockSocket.return_value
        mockSocketInstance.connect.side_effect = socket.timeout

        scanner = PortScanner("127.0.0.1", "82", 1, False, False)
        status = scanner.connect(82)

        self.assertEqual(status, "Filtered")


    def testQueue(self):
        scanner = PortScanner("127.0.0.1", "10-12", 1, False, False)
        ports = list(scanner.ports)
        self.assertEqual(ports, [10,11,12])


    @patch.object(PortScanner, 'connect', return_value="Open")
    def testStartThreading(self, mockConnect):
        scanner = PortScanner("127.0.0.1", "80-82", 3, False, False)
        
        scanner.start_threading()
        
        self.assertEqual(scanner.results[80], "Open")
        self.assertEqual(scanner.results[81], "Open")
        self.assertEqual(scanner.results[82], "Open")


    @patch('myPortScanner.socket.socket')
    def testConnectOpenPortUDP(self, mockSocket):
        # Mock the socket connection to simulate an open port
        mockSocketInstance = mockSocket.return_value
        mockSocketInstance.connect.return_value = None 

        scanner = PortScanner("127.0.0.1", "80", 1, True, False)
        status = scanner.connect(80)

        self.assertEqual(status, "Open")

    
    @patch('myPortScanner.logging.info')
    def testLogResults(self, mockLoggingInfo):
        scanner = PortScanner("127.0.0.1", "80-82", 3, False, False)
        scanner.results = {80: "Open", 81: "Closed", 82: "Filtered"}
        
        scanner.log_results()

        # Check if the logging.info method was called with the expected messages
        mockLoggingInfo.assert_any_call("Port 80: Open")
        mockLoggingInfo.assert_any_call("Port 81: Closed")
        mockLoggingInfo.assert_any_call("Port 82: Filtered")

if __name__ == "__main__":
    unittest.main()