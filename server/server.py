import socket
import threading
import json
import configparser
import time
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



# Logic Setting
ev3_logic = dict()
ev3_logic['ev3_1'] = logic.logic_ev3_1
ev3_logic['ev3_2'] = logic.logic_ev3_2
ev3_logic['ev3_3'] = logic.logic_ev3_3
ev3_logic['ev3_4'] = logic.logic_ev3_4
ev3_logic['ev3_5'] = logic.logic_ev3_5
ev3_logic['Plant_Simulation'] = logic.Simulation_data_send


while True:

    try:
        #Log Thread
        dbthread = logic.log_thread
        threading.Thread(target=dbthread, args=(data,)).start()

        client_socket, client_addr = server_socket.accept()
        ev3_name = client_socket.recv(1024).decode('utf-8')

        print(ev3_name + ' is connected')
        # threading.Thread(target=ev3_logic[ev3_name], args=(client_socket, client_addr, data)).start()
        
        if ev3_name == 'MCD_IoT':
            try:
                MCDthread = logic.MCD_IoT
                threading.Thread(target=MCDthread, args=(client_socket, client_addr, data,)).start()
            except:
                pass
        else:
            threading.Thread(target=ev3_logic[ev3_name], args=(client_socket, client_addr, data)).start()


    except:
        print('db error')
        pass

    


    


    
    





