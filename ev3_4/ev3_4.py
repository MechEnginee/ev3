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
def load_config(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)
    return config['config']['ip'], int(config['config']['port'])

# ev3 Setting
# -----------------------------------------------------------------------
# Sensor
rConv1EntrySensor = ev3.UltrasonicSensor('in1')
rConv2EntrySensor = ev3.UltrasonicSensor('in2')

# Motor
rconv1_motor = ev3.Motor('outA')
rconv2_motor = ev3.Motor('outB')
rconv_stopper_motor = ev3.Motor('outC')
rconv_push_motor = ev3.Motor('outD')

# ev3 Name
ev3_name = 'ev3_4'
# -----------------------------------------------------------------------

# Socket Setting
ip, port = load_config(ev3_name + '.ini')
address = (ip, port)

# Connecting
ev3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ev3_socket.connect(address)
ev3_socket.send(ev3_name.encode('utf-8'))

while True:
    send_data = dict()

# -----------------------------------------------------------------------
    # Get Sensor Values
    send_data['rConv1EntrySensor'] = rConv1EntrySensor.distance_centimeters
    send_data['rConv2EntrySensor'] = rConv2EntrySensor.distance_centimeters

    # Get Motor Speed
    send_data['rConv1Speed'] = rconv1_motor.speed
    send_data['rConv2Speed'] = rconv2_motor.speed
    send_data['rConv2StopperSpeed'] = rconv_stopper_motor.speed
    send_data['rConv2PushSpeed'] = rconv_push_motor.speed

    # Request
    send_data['request'] = []
    send_data['request'].append('rConv1TargetSpeed')
    send_data['request'].append('rConv2TargetSpeed')
    send_data['request'].append('rConv2StopperTargetSpeed')
    send_data['request'].append('rConv2StopperTargetDistance')
    send_data['request'].append('rConv2PushTargetSpeed')
    send_data['request'].append('rConv2PushTargetDistance')
# -----------------------------------------------------------------------

    # Make Send Data
    send_msg = json.dumps(send_data)

    # Send Data
    ev3_socket.send(send_msg.encode('utf-8'))

    # Recieve Data
    recieve_msg = ev3_socket.recv(1024).decode('utf-8')
    try:
        recieve_data = json.loads(recieve_msg)
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print ('Decoding JSON has failed')

    # Move
# -----------------------------------------------------------------------
    
    if (recieve_data['rConv1TargetSpeed']==0) and (recieve_data['rConv1TargetSpeed']==0):
        rconv1_motor.run_forever(speed_sp=0)
        rconv2_motor.run_forever(speed_sp=0)
        rconv_stopper_motor.run_to_abs_pos(speed_sp=100, position_sp=0, stop_action = 'hold')
        rconv_stopper_motor.wait_while('running')
        rconv_push_motor.run_to_abs_pos(speed_sp=100, position_sp=0, stop_action = 'hold')
        rconv_push_motor.wait_while('running')
        break
    else :
        try:
            #rconv1_motor.run_forever(speed_sp=recieve_data['rConv1TargetSpeed'])
            #rconv2_motor.run_forever(speed_sp=-recieve_data['rConv2TargetSpeed'])
            rconv_stopper_motor.run_to_abs_pos(speed_sp=recieve_data['rConv2StopperTargetSpeed'], position_sp=recieve_data['rConv2StopperTargetDistance'], stop_action = 'hold')
            rconv_push_motor.run_to_abs_pos(speed_sp=recieve_data['rConv2PushTargetSpeed'], position_sp=recieve_data['rConv2PushTargetDistance'], stop_action = 'hold')

        except:
            print('something is null')
# -----------------------------------------------------------------------

    # sleep
    time.sleep(0.1)
