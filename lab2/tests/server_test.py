import unittest
import time
from ..client import Client


# running server needed
# client.py:
# from .modules import knapsack
# from .modules import solitaire

class Servertest(unittest.TestCase):
    def test_server(self):
        client1 = Client(8081)
        time.sleep(1)
        from_server = client1.request_public_key(4983)
        self.assertEqual(None, None)
        client1.close()

        client2 = Client(8082)
        time.sleep(1)
        from_server = client2.request_public_key(8081)
        self.assertEqual(from_server, str(client1.public_key))
        client2.close()


if __name__ == '__main__':
    unittest.main()