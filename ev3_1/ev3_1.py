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
conv1_entry_sensor = ev3.ColorSensor('in1')
conv2_entry_sensor = ev3.UltrasonicSensor('in2')

# Motor
conv1_motor = ev3.Motor('outA')
conv2_motor = ev3.Motor('outB')
stopper_motor = ev3.Motor('outC')

# ev3 Name
ev3_name = 'ev3_1'
# -----------------------------------------------------------------------


# Socket Setting
ip, port = load_config(ev3_name + '.ini')
address = (ip, port)

# Connecting
ev3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ev3_socket.connect(address)
ev3_socket.send(ev3_name.encode())

while True:
    send_data = dict()

# -----------------------------------------------------------------------
    # Get Sensor Values
    send_data['eConv1EntrySensor'] = conv1_entry_sensor.reflected_light_intensity
    send_data['eConv2EntrySensor'] = conv2_entry_sensor.distance_centimeters

    # Get Motor Speed
    send_data['eConv1Speed'] = conv1_motor.speed
    send_data['eConv2Speed'] = conv2_motor.speed
    send_data['eConv2StopperSpeed'] = stopper_motor.speed

    # Request
    send_data['request'] = []
    send_data['request'].append('eConv1TargetSpeed')
    send_data['request'].append('eConv2TargetSpeed')
    send_data['request'].append('eConv2StopperTargetSpeed')
    send_data['request'].append('eConv2StopperTargetDistance')
# -----------------------------------------------------------------------

    # Make Send Data
    send_msg = json.dumps(send_data)

    # Send Data
    ev3_socket.send(send_msg.encode())

    # Recieve Data
    recieve_msg = ev3_socket.recv(1024)
    recieve_data = json.loads(recieve_msg)

    # Move
# -----------------------------------------------------------------------
    if 'eConv1TargetSpeed' in recieve_data:
        conv1_motor.run_forever(speed_sp=recieve_data['eConv1TargetSpeed'])
    
    if 'eConv2TargetSpeed' in recieve_data:
        conv1_motor.run_forever(speed_sp=recieve_data['eConv2TargetSpeed'])

    if 'eConv2StopperTargetSpeed' in recieve_data and 'eConv2StopperTargetDistance' in recieve_data:
        stopper_motor.run_to_abs_pos(speed_sp=recieve_data['eConv2StopperTargetSpeed'], position_sp=recieve_data['eConv2StopperTargetDistance'], stop_action = 'hold')
# -----------------------------------------------------------------------

    # sleep
    time.sleep(0.1)
