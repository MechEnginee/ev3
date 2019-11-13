import socket
import configparser
import json
import os
import server_ev3_util as util
import time
import datetime
# import redis


def parse_ev3_2_client_data(data):
    tM1Sensor = util.bytes_to_int(data[0:4])
    tM2Sensor = util.bytes_to_int(data[4:8])
    tM3Sensor = util.bytes_to_int(data[8:12])
    tM4Sensor = util.bytes_to_int(data[12:16])

    robotJoint1Speed = util.bytes_to_int(data[16:20])
    robotJoint2Speed = util.bytes_to_int(data[20:24])
    robotHandSpeed = util.bytes_to_int(data[24:28])

    return tM1Sensor, tM2Sensor, tM3Sensor, tM4Sensor, robotJoint1Speed, robotJoint2Speed, robotHandSpeed


def write_ev3_2_server_data(tM1Sensor, tM2Sensor, tM3Sensor, tM4Sensor, robotJoint1Speed, robotJoint2Speed, robotHandSpeed):
    data = bytes()

    data += util.int_to_bytes(tM1Sensor)
    data += util.int_to_bytes(tM2Sensor)
    data += util.int_to_bytes(tM3Sensor)
    data += util.int_to_bytes(tM4Sensor)

    data += util.int_to_bytes(robotJoint1Speed)
    data += util.int_to_bytes(robotJoint2Speed)
    data += util.int_to_bytes(robotHandSpeed)

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
# r = util.connect_redis('server_ev3.ini')

# Stopper Flag
# stopper_flag = False

while True:
    # Get Massage from EV3
    data = client_socket.recv(size)
    eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, totalConvStopSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed = parse_ev3_2_client_data(data)
    # print('{} eConv1EntrySensor-{}, eConv2EntrySensor-{}, eConv2StopperSensor-{}, totalConvStopSensor-{}, eConv1Speed-{}, eConv2Speed-{}, eConv2StopperSpeed-{}'.format(
    #     datetime.datetime.now(), eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, totalConvStopSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed
    # ))

    # # TODO: Redis
    # pipe = r.pipeline()
    
    # # Sensors
    # pipe.set('eConv1EntrySensor', eConv1EntrySensor)
    # pipe.set('eConv2EntrySensor', eConv2EntrySensor)
    # pipe.set('eConv2StopperSensor', eConv2StopperSensor)
    # pipe.set('totalConvStopSensor', totalConvStopSensor)
    # # Moter Speed
    # pipe.set('eConv1Speed', eConv1Speed)
    # pipe.set('eConv2Speed', eConv2Speed)
    # pipe.set('eConv2StopperSpeed', eConv2StopperSpeed)

    # pipe.execute()

    #TODO:
    # Motor Control
    # Conveyor
    conveyor_move_speed = util.get_robot_con1_to_testMachine1_info('move.ini')
    eConv1Speed = conveyor_move_speed
    eConv2Speed = conveyor_move_speed
    
    # Stopper
    if eConv2StopperSensor > 2:
        curr_stopper_flag = True
    else:
        curr_stopper_flag = False

    if (stopper_flag == False) and (curr_stopper_flag == True):
        eConv2StopperDist, eConv2StopperSpeed = util.get_stopper_move_info()
    elif (stopper_flag == True) and (curr_stopper_flag == False):
        eConv2StopperDist, eConv2StopperSpeed = util.get_stopper_move_info()
        eConv2StopperDist = -1 * eConv2StopperDist
    else:
        eConv2StopperDist, eConv2StopperSpeed = 0, 0
    stopper_flag = curr_stopper_flag

    # Test Code
    data = write_ev3_2_server_data(eConv1Speed, eConv2Speed, eConv2StopperDist, eConv2StopperSpeed)
    client_socket.send(data)

    # TODO: Write Log to DB
