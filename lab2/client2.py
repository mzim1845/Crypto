import socket
import pickle
import knapsack
import logging


# initializing the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


print("Type exit() to end your process")

# generating knapsack keys
(private_key, public_key) = knapsack.generate_knapsack_key_pair()

# registering to server
client_id = 8082
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.102', 8080))
data_string = pickle.dumps([client_id, public_key])
logging.info("Client with " + str(client_id) + " id and " + str(private_key) + " " + str(public_key) + " keys")
client.send(data_string)
logging.info("Client registered")


# console-based communication with the client
while True:
    message = input("Which client do you want to get in touch with?\n")
    if message == "exit()":
        client.send(message.encode())
        client.close()
        exit()

    client.send(message.encode())
    from_server = client.recv(2048).decode()
    if from_server == "not found":
        logging.info('Searched client is not registered')
    else:
        logging.info('Searched client is registered: ' + str(from_server))