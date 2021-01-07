import socket
import pickle
from modules import knapsack
from modules import solitaire
import logging


def initialize_logger():
    # Initializing the logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def request_port(request_question):
    while True:
        try:
            client_input = input(request_question)
            if client_input == 'exit()':
                exit()
            else:
                port = int(client_input)
                if port < 1024 or port > 49151:
                    print('Port must be a number between 1024 and 49151')
                else:
                    break
        except ValueError:
            print('Port must be a number between 1024 and 49151')

    return port


class Client:

    def __init__(self, port):
        self.port = port
        # generating knapsack keys
        (self.private_key, self.public_key) = knapsack.generate_knapsack_key_pair()

        # register to server
        self.client_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not self.bind_to_port(8080, self.client_to_server):
            exit()
        data_string = pickle.dumps([port, self.public_key])
        logging.info('Client ' + str(port) + ': ' + str(self.private_key) + ' ' + str(self.public_key) + ' keys')
        self.client_to_server.send(data_string)

    def bind_to_port(self, port, csocket):
        try:
            csocket.connect(('127.0.0.1', port))
            return True
        except ConnectionRefusedError:
            print('Couldn\'t connect')
            return False

    def request_public_key(self, partner_port):
        self.client_to_server.send(str(partner_port).encode())
        from_server = self.client_to_server.recv(2048).decode()
        if from_server == 'NOT FOUND':
            print('Searched client is not registered')
        else:
            print('Searched client is registered: ' + str(from_server))
            return eval(from_server)

    def wait_for_hello(self):
        client_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_to_client.bind(('127.0.0.1', self.port))
        client_to_client.listen(5)

        logging.info('Client ' + str(self.port) + ': waiting for HELLO')

        connection, address = client_to_client.accept()
        from_client = connection.recv(2048)
        decrypted_message = knapsack.decrypt_mh(eval(from_client.decode()), self.private_key).split()
        if decrypted_message[0] == 'HELLO' and len(decrypted_message) == 2:
            logging.info('Client ' + str(self.port) + ': ' + 'received message says HELLO' + decrypted_message[1])
            client_to_client.close()
            return decrypted_message[1]
        else:
            logging.info('Client ' + str(self.port) + ': ' + 'received message doesn\'t say HELLO')
            client_to_client.close()
            return ''

    def wait_for_ack(self, partner_port):
        client_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_to_client.bind(('127.0.0.1', self.port))
        client_to_client.listen(5)

        logging.info('Client ' + str(self.port) + ': ' + 'waiting for ACK from ' + str(partner_port))

        connection, address = client_to_client.accept()
        from_client = connection.recv(2048)
        if from_client:
            decrypted_message = knapsack.decrypt_mh(eval(from_client.decode()), self.private_key)
            if decrypted_message == 'ACK ' + str(partner_port):
                logging.info('Client ' + str(self.port) + ': ' + 'received message says ' + decrypted_message)
                client_to_client.close()
                return True
            else:
                logging.info('Client ' + str(self.port) + ': ' + 'received message doesn\'t say ACK ' + partner_port)
                client_to_client.close()
                return False
        else:
            print('Connection error')
            client_to_client.close()
            return False

    def wait_for_half_secret_key(self):
        client_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_to_client.bind(('127.0.0.1', self.port))
        client_to_client.listen(5)

        logging.info('Client ' + str(self.port) + ': ' + 'waiting for SECRET from partner')

        connection, address = client_to_client.accept()
        from_client = connection.recv(2048)
        decrypted_message = knapsack.decrypt_mh(eval(from_client.decode()), self.private_key).split()
        if decrypted_message[0] == 'SECRET' and len(decrypted_message) == 2:
            logging.info('Client ' + str(self.port) + ': ' + 'received message says SECRET ' + decrypted_message[1])
            return decrypted_message[1]
        else:
            logging.info('Client ' + str(self.port) + ': ' + 'received message doesn\'t contain half secret key')
            return ''

    def send_specific_message(self, partner_port, partner_pub_key, message):
        client_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not self.bind_to_port(partner_port, client_to_client):
            return
        client_to_client.send(str(knapsack.encrypt_mh(message.encode(), partner_pub_key)).encode())
        client_to_client.close()

    def close(self):
        self.client_to_server.close()


def main():
    initialize_logger()

    logging.info('Client started')
    print('>>>Type exit() to end your process<<<')
    port = request_port('What is your port number?\n')
    client = Client(port)


    # console-based communication with the client
    while True:
        answer = input('Do you want to send or receive message?(send/receive)\n')

        try:
            if answer == 'send':
                partner_port = request_port('Which client do you want to get in touch with?\n')
                partner_public_key = client.request_public_key(partner_port)

                if partner_public_key:
                    logging.info('Client ' + str(port) + ': sending HELLO')
                    try:
                        client.send_specific_message(partner_port, partner_public_key, 'HELLO ' + str(port))
                        if client.wait_for_ack(partner_port):
                            half_secret_key1 = solitaire.generate_random_secret()
                            client.send_specific_message(partner_port, partner_public_key, 'SECRET ' + half_secret_key1)
                            half_secret_key2 = client.wait_for_half_secret_key()
                            common_secret_key = solitaire.generate_common_secret(half_secret_key1, half_secret_key2)
                    except ConnectionResetError:
                        print('Connection error')

            elif answer == 'receive':
                partner_port = int(client.wait_for_hello())
                if partner_port:
                    partner_public_key = client.request_public_key(partner_port)
                    if partner_public_key:
                        client.send_specific_message(partner_port, partner_public_key, 'ACK ' + str(port))
                        half_secret_key2 = client.wait_for_half_secret_key()
                        if half_secret_key2:
                            half_secret_key1 = solitaire.generate_random_secret()
                            client.send_specific_message(partner_port, partner_public_key, 'SECRET ' + half_secret_key1)
                            common_secret_key = solitaire.generate_common_secret(half_secret_key2, half_secret_key1)

            elif answer == 'exit()':
                client.close()
                exit()
        except ConnectionResetError:
            print('Server stopped')
            client.close()
            exit()


if __name__ == '__main__':
    main()