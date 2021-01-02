import socket
import pickle
import logging


def help_client(conn, client_id):

    found_client_ind = [keys.index(client) for client in keys if client[0] == client_id[0]]
    if found_client_ind:
        logging.info(str(client_id[0]) + " client already registered")
        keys[found_client_ind[0]][1] = client_id[1]
    else:
        logging.info(str(client_id[0]) + " client registered")
        keys.append(client_id)

    data_recv = conn.recv(2048)
    message = int(data_recv.decode())
    found_client = [client for client in keys if client[0] == message]
    print(found_client)
    if not found_client:
        logging.info(str(client_id[0]) + " looking for: " + str(message) + " not found")
        conn.send("not found".encode())
    else:
        logging.info(str(client_id[0]) + " looking for: " + str(message) + " found")
        conn.send(str(found_client[0][1]).encode())
    conn.close()

# Initializing the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

keys = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('192.168.0.102', 8080))
server.listen(5)

while True:
    connection, address = server.accept()
    from_client = connection.recv(2048)
    id_data = pickle.loads(from_client)
    logging.info("Client to register: " + str(id_data))
    help_client(connection, id_data)
