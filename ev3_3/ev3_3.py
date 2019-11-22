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
tM4_sensor = ev3.ColorSensor('in1')
tM3_sensor = ev3.ColorSensor('in2')

# Motor


# ev3 Name
ev3_name = 'ev3_3'
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
    send_data['tM3_sensor'] = tM3_sensor.reflected_light_intensity
    send_data['tM4_sensor'] = tM4_sensor.reflected_light_intensity

    # Get Motor Speed

    # Request
# -----------------------------------------------------------------------

    # Make Send Data
    send_msg = json.dumps(send_data)

    # Send Data
    ev3_socket.send(send_msg.encode('utf-8'))

    # Recieve Data
    #recieve_msg = ev3_socket.recv(1024).decode('utf-8')
    #recieve_data = json.loads(recieve_msg)

    # Move
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------

    # sleep
    time.sleep(0.1)
