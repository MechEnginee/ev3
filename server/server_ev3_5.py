import socket
import configparser
import json
import os
import server_ev3_util as util
import time
import datetime
import redis


def parse_ev3_5_client_data(data):
    rConv2StopperSensor = util.bytes_to_int(data[0:4])
    totalConvStopSensor = util.bytes_to_int(data[4:8])

    
    return rConv2StopperSensor, totalConvStopSensor


def write_ev3_5_server_data(rConv2StopperSensor, totalConvStopSensor):
    data = bytes()

    data += util.int_to_bytes(rConv2StopperSensor)
    data += util.int_to_bytes(totalConvStopSensor)

    return data


# Config
ip, port, size = util.load_config('server_ev3.ini')
address = (ip, port)
print('Server IP : {} / Port : {}'.format(ip, port))

# Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)

server_socket.listen()
client_socket, client_addr = server_socket.accept()

# Redis
r = util.connect_redis('server_ev3.ini')

# Stopper Flag
stopper_flag = False

while True:
    # Get Massage from EV3
    data = client_socket.recv(size)
    rConv2StopperSensor, totalConvStopSensor = parse_ev3_5_client_data(data)
    
    print('{} eConv1EntrySensor-{}, eConv2EntrySensor-{}, eConv2StopperSensor-{}, totalConvStopSensor-{}, eConv1Speed-{}, eConv2Speed-{}, eConv2StopperSpeed-{}'.format(
        datetime.datetime.now(), rConv2StopperSensor, totalConvStopSensor
    ))

    # TODO: Redis
    pipe = r.pipeline()
    
    # Sensors
    pipe.set('rConv2StopperSensor', rConv2StopperSensor)
    pipe.set('totalConvStopSensor', totalConvStopSensor)
    #pipe.set('eConv2StopperSensor', eConv2StopperSensor)
    #pipe.set('totalConvStopSensor', totalConvStopSensor)
    # Moter Speed
 
    #ev3_2_stopper_sensor_Info


    pipe.execute()

    # Motor Control
    # Conveyor
    # conveyor_move_speed = util.get_conveyor_move_speed('move.ini')
    # eConv1Speed = conveyor_move_speed
    # eConv2Speed = conveyor_move_speed
    
    # Test Code
    data = write_ev3_5_server_data(rConv2StopperSensor, totalConvStopSensor)
    client_socket.send(data)

    # TODO: Write Log to DB
