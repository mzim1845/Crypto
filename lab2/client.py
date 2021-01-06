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


class Client:

    @staticmethod
    def bind_to_port(client, port):
        try:
            client.connect(('127.0.0.1', port))
            return True
        except ConnectionRefusedError:
            print('Couldn\'t connect')
            return False

    @staticmethod
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

    @staticmethod
    def request_public_key(client_to_server, partner_port):
        try:
            client_to_server.send(str(partner_port).encode())
            from_server = client_to_server.recv(2048).decode()
            if from_server == 'NOT FOUND':
                print('Searched client is not registered')
            else:
                print('Searched client is registered: ' + str(from_server))
                return pickle.loads(from_server)
        except ConnectionResetError:
            print('Server stopped')
            client_to_server.close()
            exit()

    @staticmethod
    def wait_for_hello(client_port, private_key):
        client_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_to_client.bind(('127.0.0.1', client_port))
        client_to_client.listen(5)

        logging.info('Client ' + str(client_port) + ': waiting for HELLO')

        connection, address = client_to_client.accept()
        from_client = connection.recv(2048)
        decrypted_message = knapsack.decrypt_mh(from_client.decode(), private_key).split()
        logging.info('Client ' + str(client_port) + ': ' + 'received message is ' + decrypted_message)
        if decrypted_message == 'HELLO ' and len(decrypted_message) == 2:
            logging.info('Client ' + str(client_port) + ': ' + 'received message says HELLO' + decrypted_message[1])
            return decrypted_message[1]
        else:
            logging.info('Client ' + str(client_port) + ': ' + 'received message doesn\'t say HELLO')
            return ''

    @staticmethod
    def wait_for_ack(client_port, partner_port, private_key):
        client_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_to_client.bind(('127.0.0.1', client_port))
        client_to_client.listen(5)

        logging.info('Client ' + str(client_port) + ': ' + 'waiting for ACK from' + str(partner_port))

        connection, address = client_to_client.accept()
        from_client = connection.recv(2048)
        decrypted_message = knapsack.decrypt_mh(from_client.decode(), private_key)
        logging.info('Client ' + str(client_port) + ': ' + 'received message is ' + decrypted_message)
        if decrypted_message == 'ACK ' + partner_port:
            logging.info('Client ' + str(client_port) + ': ' + 'received message says ' + decrypted_message)
            return True
        else:
            logging.info('Client ' + str(client_port) + ': ' + 'received message doesn\'t say ACK' + partner_port)
            return False

    @staticmethod
    def wait_for_half_secret_key(client_port, private_key):
        client_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_to_client.bind(('127.0.0.1', client_port))
        client_to_client.listen(5)

        logging.info('Client ' + str(client_port) + ': ' + 'waiting for SECRET from' + str(client_port))

        connection, address = client_to_client.accept()
        from_client = connection.recv(2048)
        decrypted_message = knapsack.decrypt_mh(from_client.decode(), private_key).split()
        logging.info('Client ' + str(client_port) + ': ' + 'received message is ' + decrypted_message)
        if decrypted_message[0] == 'SECRET' and len(decrypted_message) == 2:
            logging.info('Client ' + str(client_port) + ': ' + 'received message says SECRET' + decrypted_message[1])
            return decrypted_message[1]
        else:
            logging.info('Client ' + str(client_port) + ': ' + 'received message doesn\'t contain half secret key')
            return ''

    @staticmethod
    def send_specific_message(self, partner_port, partner_pub_key, message):

        client_to_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not self.bind_to_port(client_to_client, partner_port):
            return
        client_to_client.send(knapsack.encrypt_mh(message, partner_pub_key))
        client_to_client.close()


def main():
    initialize_logger()

    client = Client()
    logging.info('Client started')
    print('>>>Type exit() to end your process<<<')
    client_port = client.request_port('What is your port number?\n')

    # generating knapsack keys
    (private_key, public_key) = knapsack.generate_knapsack_key_pair()

    # register to server
    client_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if not client.bind_to_port(client_to_server, 8080):
        exit()
    data_string = pickle.dumps([client_port, public_key])
    logging.info('Client ' + str(client_port) + ': ' + str(private_key) + ' ' + str(public_key) + ' keys')
    client_to_server.send(data_string)


    # console-based communication with the client
    while True:
        answer = input('Do you want to send or receive message?(send/receive)\n')

        if answer == 'send':
            partner_port = client.request_port('Which client do you want to get in touch with?\n')
            partner_public_key = client.request_public_key(client_to_server, partner_port)
            logging.info('Client ' + str(client_port) + ': received partner\'s public key'
                                 + str(partner_public_key))

            logging.info('Client ' + str(client_port) + ': sending HELLO')
            client.send_specific_message(client, partner_port, partner_public_key, 'HELLO ' + str(client_port))
            client.wait_for_ack(client_port, partner_port, private_key)
            half_secret_key1 = solitaire.generate_random_secret()
            client.send_specific_message(client, client_port, private_key, 'SECRET ' + half_secret_key1)
            half_secret_key2 = client.wait_for_half_secret_key(client_port, private_key)
            common_secret_key = solitaire.generate_common_secret(half_secret_key1, half_secret_key2)

        elif answer == 'receive':
            logging.info('Client ' + str(client_port) + ': waiting for HELLO')
            partner_port = client.wait_for_hello(client_port, private_key)
            partner_public_key = client.request_public_key(client_to_server, partner_port)
            client.send_specific_message(client, partner_port, partner_public_key, 'ACK ' + str(client_port))
            half_secret_key2 = client.wait_for_half_secret_key(client_port, private_key)
            half_secret_key1 = solitaire.generate_random_secret()
            client.send_specific_message(client, client_port, private_key, 'SECRET ' + half_secret_key1)
            common_secret_key = solitaire.generate_common_secret(half_secret_key1, half_secret_key2)


if __name__ == '__main__':
    main()