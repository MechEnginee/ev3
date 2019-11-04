import socket
import configparser
import json


def load_ip_port(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)
    return config['config']['ip'].replace('"', ''), int(config['config']['port']), int(config['config']['size'])



# Socket Setting
ip, port, size = load_ip_port('ev3_1.ini')
address = (ip, port)
print('Server IP : {} / Port : {}'.format(ip, port))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)

# Waiting
server_socket.listen()
client_socket, client_addr = server_socket.accept()

for inx in range(10):
    # Get Massage from EV#
    msg = client_socket.recv(size).decode()
    print("[{}] message : {}".format(client_addr,msg))

    # TODO: Redis 연동







    # Data Processing
    # TODO: 센서 및 모터 값 기반 행동 작성 @박태진사원
    data = json.loads(msg)
    sensors = data['sensors']
    sensors['eConv1EntrySensor'] = not sensors['eConv1EntrySensor']
    sensors['eConv2EntrySensor'] = not sensors['eConv2EntrySensor']
    sensors['eConv2StopperSensor'] = not sensors['eConv2StopperSensor']
    sensors['eConv2TMInputSensor'] = not sensors['eConv2TMInputSensor']

    speeds = data['speeds']
    speeds['eConv1Speed'] = -1 * speeds['eConv1Speed']
    speeds['eConv2Speed'] = -1 * speeds['eConv2Speed']
    speeds['eConv2StopperSpeed'] = -1 * speeds['eConv2StopperSpeed']
    
    client_socket.send(json.dumps(data).encode())
    
