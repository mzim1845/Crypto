import unittest
from ..server import Server


class Servertest(unittest.TestCase):
    def test_server(self):
        server = Server('127.0.0.1', 8080)
        server.start_listening()




if __name__ == '__main__':
    unittest.main()