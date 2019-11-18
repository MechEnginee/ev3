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


def parse_ev3_1_server_data(data):
    eConv1Speed = bytes_to_int(data[0:4])
    eConv2Speed = bytes_to_int(data[4:8])
    eConv2StopperDist = bytes_to_int(data[8:12])
    eConv2StopperSpeed = bytes_to_int(data[12:16])
    #TODO: totalConvStopSensor Pull

    return eConv1Speed, eConv2Speed, eConv2StopperDist, eConv2StopperSpeed

def write_ev3_1_client_data(eConv1EntrySensor, eConv2EntrySensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed):
    data = bytes()

    data += int_to_bytes(eConv1EntrySensor)
    data += float_to_bytes(eConv2EntrySensor)
    # data += int_to_bytes(eConv2StopperSensor)
    # data += int_to_bytes(totalConvStopSensor)

    data += int_to_bytes(eConv1Speed)
    data += int_to_bytes(eConv2Speed)
    data += int_to_bytes(eConv2StopperSpeed)

    return data
# -----------------------------------------------------------------------

# ev3 Setting
# Motor
conv1_motor = ev3.Motor('outA')
conv2_motor = ev3.Motor('outB')
stopper_motor = ev3.Motor('outC')

# Sensor
conv1_entry_sensor = ev3.ColorSensor('in1')
conv2_entry_sensor = ev3.UltrasonicSensor('in2')
# stopper_sensor = ev3.ColorSensor('in3')
# emergency_sensor = ev3.TouchSensor('in4')

# Socket Setting
ip, port, size = load_config('ev3_1.ini')
address = (ip, port)

# Connecting
ev3_1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ev3_1_socket.connect(address)

while True:
    # Get Sensor Values
    eConv1EntrySensor = conv1_entry_sensor.reflected_light_intensity
    eConv2EntrySensor = conv2_entry_sensor.distance_centimeters
    # eConv2StopperSensor = stopper_sensor.reflected_light_intensity
    # totalConvStopSensor = emergency_sensor.value()

    # Get Motor Speed
    eConv1Speed = conv1_motor.speed
    eConv2Speed = conv2_motor.speed
    eConv2StopperSpeed = stopper_motor.speed

    # Make Send Data
    data = write_ev3_1_client_data(eConv1EntrySensor, eConv2EntrySensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed)

    # Send Data
    ev3_1_socket.send(data)

    # Recieve Data
    data = ev3_1_socket.recv(size)
    eConv1Speed, eConv2Speed, eConv2StopperDist, eConv2StopperSpeed = parse_ev3_1_server_data(data)
    # print('{} eConv1EntrySensor-{}, eConv2EntrySensor-{}, eConv2StopperSensor-{}, totalConvStopSensor-{}, eConv1Speed-{}, eConv2Speed-{}, eConv2StopperSpeed-{}'.format(
    #     datetime.datetime.now(), eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, totalConvStopSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed
    # ))

    # Move Motor
    print(stopper_motor.position_sp, type(stopper_motor.position_sp), file=sys.stderr)
    if totalConvStopSensor == 1:
        conv1_motor.run_forever(speed_sp=0)
        conv2_motor.run_forever(speed_sp=0)
        if stopper_motor.position_sp<0: # emergency initiate
            a = abs(stopper_motor.position_sp)#Back Direction
            stopper_motor.run_to_rel_pos(speed_sp=300, position_sp=a)
            stopper_motor.wait_while('running')
            time.sleep(3)
        elif stopper_motor.position_sp>=0: # emergency initiate
            stopper_motor.wait_while('running') 
            time.sleep(3)
        
        break

    else:
        conv1_motor.run_forever(speed_sp=eConv1Speed)
        conv2_motor.run_forever(speed_sp=-1*eConv2Speed)

        if (eConv2StopperDist == 0) and (eConv2StopperSpeed == 0):
            pass
        else:   
            stopper_motor.run_to_rel_pos(speed_sp=eConv2StopperSpeed, position_sp=eConv2StopperDist)

    # sleep
    time.sleep(0.1)
