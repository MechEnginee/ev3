import socket
import threading
import json
import configparser
import logic


def load_server_ip_port(ini_path='server.ini'):
    config = configparser.ConfigParser()
    config.read(ini_path)
    return config['server']['ip'], int(config['server']['port'])

# Socket Initializing
address = load_server_ip_port()
print(address)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(10)

# Data
data = dict()

# # Log Thread
# threading.Thread(target=log_thread, args=(data)).start()

# Logic Setting
ev3_logic = dict()
ev3_logic['ev3_1'] = logic.logic_ev3_1
ev3_logic['ev3_2'] = logic.logic_ev3_2
ev3_logic['ev3_3'] = logic.logic_ev3_3
ev3_logic['ev3_4'] = logic.logic_ev3_4
ev3_logic['ev3_5'] = logic.logic_ev3_5


while True:
    client_socket, client_addr = server_socket.accept()
    ev3_name = client_socket.recv(1024).decode('utf-8')

    print(ev3_name + ' is connected')
    threading.Thread(target=ev3_logic[ev3_name], args=(client_socket, client_addr, data)).start()


