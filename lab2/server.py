import socket
import pickle
import logging
import tracemalloc
from _thread import *

# list of (port, public key)s
keys = []

def initialize_logger():
    # Initializing the logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_listening(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        logging.info("Server started, waiting for clients...")

        # receiving connections
        while True:
                connection, address = server.accept()
                from_client = connection.recv(2048)
                data_recv = pickle.loads(from_client)
                logging.info("New client: " + str(data_recv))
                start_new_thread(self.client_handler, (connection, data_recv))

    @staticmethod
    def register_client(client_data):
        # checking if client is already registered
        client_ind = [keys.index(client) for client in keys if client[0] == client_data[0]]
        if client_ind:
            logging.info("Client " + str(client_data[0]) + ": " + "already registered")
            keys[client_ind[0]][1] = client_data[1]
        else:  # new client
            logging.info("Client " + str(client_data[0]) + ": " + "newly registered")
            keys.append(client_data)

    @staticmethod
    def remove_client(client_data):
        client_ind = [keys.index(client) for client in keys if client[0] == client_data[0]]
        if client_ind:
            return keys.remove(client_data)

    def client_handler(self, conn, client_data):
        self.register_client(client_data)
        while True:
            try:
                data_recv = conn.recv(2048)
                if data_recv:
                    message = int(data_recv.decode())

                    found_client = [client for client in keys if client[0] == message]
                    if not found_client:
                        logging.info("Client " + str(client_data[0]) + ": looking for "
                                             + str(message) + " - not found")
                        conn.send("NOT FOUND".encode())
                    else:
                        logging.info("Client " + str(client_data[0]) + ": looking for "
                                             + str(message) + " - found")
                        conn.send(str(found_client[0][1]).encode())
                else:
                    logging.info("Client " + str(client_data[0]) + ": exited")
                    self.remove_client(client_data)
                    break
            except ConnectionResetError:
                logging.info("Client " + str(client_data[0]) + ": exited")
                self.remove_client(client_data)
                break
        exit_thread()
        conn.close()


def main():
    initialize_logger()
    server = Server('127.0.0.1', 8080)
    server.start_listening()


if __name__ == '__main__':
    main()