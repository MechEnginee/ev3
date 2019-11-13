import os
import sys
import socket
import time
import configparser
import json
import struct
import datetime

import ev3dev.ev3 as ev3

# Utility Functions
# -----------------------------------------------------------------------
def int_to_bytes(v):
    return v.to_bytes(4, 'big', signed=True)

def float_to_bytes(v):
    return struct.pack('!f', v)

def bool_to_bytes(b):
    return b.to_bytes(1, 'big')

def bytes_to_int(b):
    return int.from_bytes(b, 'big', signed=True)

def bytes_to_float(b):
    return struct.unpack('!f', b)[0]

def bytes_to_bool(b):
    return bool.from_bytes(b, 'big')


def load_config(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)
    return config['config']['ip'], int(config['config']['port']), int(config['config']['size'])


def parse_ev3_2_server_data(data):
    tM1Sensor = bytes_to_int(data[0:4])
    tM2Sensor = bytes_to_int(data[4:8])
    tM3Sensor = bytes_to_int(data[8:12])
    tM4Sensor = bytes_to_int(data[12:16])

    robotJoint1Speed = bytes_to_int(data[16:20])
    robotJoint2Speed = bytes_to_int(data[20:24])
    robotHandSpeed = bytes_to_int(data[24:28])

    return tM1Sensor, tM2Sensor, tM3Sensor, tM4Sensor, robotJoint1Speed, robotJoint2Speed, robotHandSpeed


def write_ev3_2_client_data(tM1Sensor, tM2Sensor, tM3Sensor, tM4Sensor, robotJoint1Speed, robotJoint2Speed, robotHandSpeed):
    data = bytes()

    data += int_to_bytes(tM1Sensor)
    data += int_to_bytes(tM2Sensor)
    data += int_to_bytes(tM3Sensor)
    data += int_to_bytes(tM4Sensor)

    data += int_to_bytes(robotJoint1Speed)
    data += int_to_bytes(robotJoint2Speed)
    data += int_to_bytes(robotHandSpeed)

    return data
# -----------------------------------------------------------------------

# ev3 Setting
# Motor
Robot_Base_Motor = ev3.Motor('outA')
Robot_Elbow_Motor = ev3.Motor('outB')
Robot_Hand_Motor = ev3.Motor('outC')

# Sensor
Test_Machine1 = ev3.ColorSensor('in1')
Test_Machine2 = ev3.ColorSensor('in2')
Test_Machine3 = ev3.ColorSensor('in3')
Test_Machine4 = ev3.ColorSensor('in4')

# Socket Setting
ip, port, size = load_config('ev3_2.ini')
address = (ip, port)

# Connecting
ev3_2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ev3_2_socket.connect(address)

while True:
    # Get Sensor Values
    tM1Sensor = Test_Machine1.reflected_light_intensity
    tM2Sensor = Test_Machine2.reflected_light_intensity
    tM3Sensor = Test_Machine3.reflected_light_intensity
    tM4Sensor = Test_Machine4.reflected_light_intensity

    # Get Motor Speed
    robotJoint1Speed = Robot_Base_Motor.speed
    robotJoint2Speed = Robot_Elbow_Motor.speed
    robotHandSpeed = Robot_Hand_Motor.speed

    # Make Send Data
    data = write_ev3_2_client_data(tM1Sensor, tM2Sensor, tM3Sensor, tM4Sensor, robotJoint1Speed, robotJoint2Speed, robotHandSpeed)

    # Send Data
    ev3_2_socket.send(data)

    # Recieve Data
    data = ev3_2_socket.recv(size)
    tM1Sensor, tM2Sensor, tM3Sensor, tM4Sensor, robotJoint1Speed, robotJoint2Speed, robotHandSpeed = parse_ev3_2_server_data(data)
    # print('{} eConv1EntrySensor-{}, eConv2EntrySensor-{}, eConv2StopperSensor-{}, totalConvStopSensor-{}, eConv1Speed-{}, eConv2Speed-{}, eConv2StopperSpeed-{}'.format(
    #     datetime.datetime.now(), eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, totalConvStopSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed
    # ))

    #TODO: Move Motor
    # print(stopper_motor.position_sp, type(stopper_motor.position_sp), file=sys.stderr)
    # if totalConvStopSensor == 1:
    #     # conv1_motor.run_forever(speed_sp=0)
    #     # conv2_motor.run_forever(speed_sp=0)
    #     if stopper_motor.position_sp<0: # emergency initiate
    #         a = abs(stopper_motor.position_sp)
    #         stopper_motor.run_to_rel_pos(speed_sp=300, position_sp=a) 
    #         stopper_motor.wait_while('running')
    #         time.sleep(3)
    #     elif stopper_motor.position_sp>=0: # emergency initiate
    #         stopper_motor.wait_while('running') 
    #         time.sleep(3)
        
    #     break

    # else:
    #     # conv1_motor.run_forever(speed_sp=eConv1Speed)
    #     # conv2_motor.run_forever(speed_sp=-1*eConv2Speed)

    #     if (eConv2StopperDist == 0) and (eConv2StopperSpeed == 0):
    #         pass
    #     else:   
    #         stopper_motor.run_to_rel_pos(speed_sp=eConv2StopperSpeed, position_sp=eConv2StopperDist)

    # sleep
    time.sleep(0.1)
