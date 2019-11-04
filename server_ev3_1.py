import socket
import configparser
import json
import os
import server_ev3_util as util


def parse_data_ev3_1(data):
    eConv1EntrySensor = util.bytes_to_bool(data[0:1])
    eConv2EntrySensor = util.bytes_to_bool(data[1:2])
    eConv2StopperSensor = util.bytes_to_bool(data[2:3])
    eConv2TMInputSensor = util.bytes_to_bool(data[3:4])

    eConv1Speed = util.bytes_to_float(data[4:8])
    eConv2Speed = util.bytes_to_float(data[8:12])
    eConv2StopperSpeed = util.bytes_to_float(data[12:16])

    return eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, eConv2TMInputSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed


def write_data_ev3_1(eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, eConv2TMInputSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed):
    data = bytes()

    data += util.bool_to_bytes(eConv1EntrySensor)
    data += util.bool_to_bytes(eConv2EntrySensor)
    data += util.bool_to_bytes(eConv2StopperSensor)
    data += util.bool_to_bytes(eConv2TMInputSensor)

    data += util.float_to_bytes(eConv1Speed)
    data += util.float_to_bytes(eConv2Speed)
    data += util.float_to_bytes(eConv2StopperSpeed)

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

while True:
    # Get Massage from EV3
    data = client_socket.recv(size)
    eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, eConv2TMInputSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed = parse_data_ev3_1(data)

    # TODO: Redis






    # TODO: Motor Control





    # TODO: Write Log to DB







    # Test Code
    data = write_data_ev3_1(eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, eConv2TMInputSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed)
    client_socket.send(data)
