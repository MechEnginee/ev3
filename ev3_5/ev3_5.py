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
    return config['config']['ip'].replace('"', ''), int(config['config']['port']), int(config['config']['size'])


def parse_ev3_5_server_data(data):
    eConv2StopperSensor = bytes_to_int(data[0:4])
    totalConvStopSensor = bytes_to_int(data[4:8])

    return eConv2StopperSensor, totalConvStopSensor

def write_ev3_5_client_data(eConv2StopperSensor, totalConvStopSensor):
    data = bytes()

    data += int_to_bytes(eConv2StopperSensor)
    data += int_to_bytes(totalConvStopSensor)

    return data
# -----------------------------------------------------------------------

# ev3 Setting
# Motor

# Sensor
stopper_sensor = ev3.ColorSensor('in1')
emergency_sensor = ev3.TouchSensor('in2')

# Socket Setting
ip, port, size = load_config('ev3_5.ini')
address = (ip, port)

# Connecting
ev3_5_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ev3_5_socket.connect(address)

while True:
    # Get Sensor Values
    rConv2StopperSensor = stopper_sensor.reflected_light_intensity
    totalConvStopSensor = emergency_sensor.value()

    # Get Motor Speed

    # Make Send Data
    data = write_ev3_5_client_data(rConv2StopperSensor, totalConvStopSensor)

    # Send Data
    ev3_5_socket.send(data)

    # Recieve Data
    # data = ev3_5_socket.recv(size)
    # rConv2StopperSensor, totalConvStopSensor = parse_ev3_5_server_data(data)

    # print('{} eConv1EntrySensor-{}, eConv2EntrySensor-{}, eConv2StopperSensor-{}, totalConvStopSensor-{}, eConv1Speed-{}, eConv2Speed-{}, eConv2StopperSpeed-{}'.format(
    #     datetime.datetime.now(), eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, totalConvStopSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed
    # ))

    # Move Motor
    # print(stopper_motor.position_sp, type(stopper_motor.position_sp), file=sys.stderr)
    # if totalConvStopSensor == 1:
    #     conv1_motor.run_forever(speed_sp=0)
    #     conv2_motor.run_forever(speed_sp=0)
    #     if stopper_motor.position_sp<0: # emergency initiate
    #         a = abs(stopper_motor.position_sp)#Back Direction
    #         stopper_motor.run_to_rel_pos(speed_sp=300, position_sp=a) 
    #         stopper_motor.wait_while('running')
    #         time.sleep(3)
    #     elif stopper_motor.position_sp>=0: # emergency initiate
    #         stopper_motor.wait_while('running') 
    #         time.sleep(3)
        
    #     break

    # else:
    #     conv1_motor.run_forever(speed_sp=eConv1Speed)
    #     conv2_motor.run_forever(speed_sp=-1*eConv2Speed)

    #     if (eConv2StopperDist == 0) and (eConv2StopperSpeed == 0):
    #         pass
    #     else:   
    #         stopper_motor.run_to_rel_pos(speed_sp=eConv2StopperSpeed, position_sp=eConv2StopperDist)

    # sleep
    time.sleep(0.1)
