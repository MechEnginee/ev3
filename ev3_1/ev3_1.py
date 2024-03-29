import os
import sys
import socket
import time
import configparser
import json
import struct
import datetime
import threading
import ev3dev.ev3 as ev3

# switch1 = False
# switch3 = False
# Flag1 = False
# Flag3 = False

# Utility Functions
def load_config(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)
    return config['config']['ip'], int(config['config']['port'])

# def test1_timer():
#     global Flag1
#     global switch1
#     time.sleep(5)
#     Flag1 = True
    

# def test3_timer():
#     global Flag3
#     global switch3
#     time.sleep(5)
#     Flag3 = True

# ev3 Setting
# -----------------------------------------------------------------------
# Sensor
conv1_entry_sensor = ev3.ColorSensor('in1')
conv2_entry_sensor = ev3.UltrasonicSensor('in2')
tM1_sensor = ev3.ColorSensor('in3')
tM3_sensor = ev3.ColorSensor('in4')

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
ev3_socket.send(ev3_name.encode('utf-8'))

while True:
    send_data = dict()

# -----------------------------------------------------------------------
    # Get Sensor Values
    send_data['eConv1EntrySensor'] = conv1_entry_sensor.reflected_light_intensity
    send_data['eConv2EntrySensor'] = conv2_entry_sensor.distance_centimeters
    if conv1_entry_sensor.reflected_light_intensity > 0.5:
        send_data['eConv1EntrySensor'] = 1
    else:
        send_data['eConv1EntrySensor'] = 0
    
    if conv2_entry_sensor.distance_centimeters <= 9.3:
        send_data['eConv2EntrySensor'] = 1
    else:
        send_data['eConv2EntrySensor'] = 0

    tM1value = tM1_sensor.reflected_light_intensity
    tM3value = tM3_sensor.reflected_light_intensity

    if tM1value > 3:
        send_data['tM1Sensor'] = 1
    else:
        send_data['tM1Sensor'] = 0

    if tM3value > 3:
        send_data['tM3Sensor'] = 1
    else:
        send_data['tM3Sensor'] = 0


    # Get Motor Speed
    send_data['eConv1Speed'] = conv1_motor.speed
    send_data['eConv2Speed'] = conv2_motor.speed
    send_data['eConv2StopperSpeed'] = stopper_motor.speed

    # Request
    send_data['request'] = []
    send_data['request'].append('totalConvStopSensor')
    send_data['request'].append('eConv1TargetSpeed')
    send_data['request'].append('eConv2TargetSpeed')
    send_data['request'].append('eConv2StopperTargetSpeed')
    send_data['request'].append('eConv2StopperTargetDistance')
    send_data['request'].append('totalConvStopSensor')
# -----------------------------------------------------------------------

    # Make Send Data
    send_msg = json.dumps(send_data)

    # Send Data
    ev3_socket.send(send_msg.encode('utf-8'))

    # Recieve Data
    try:
        recieve_msg = ev3_socket.recv(1024).decode('utf-8')
        recieve_data = json.loads(recieve_msg)
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print ('Decoding JSON has failed')

    # Move
# -----------------------------------------------------------------------
    if 'totalConvStopSensor' in recieve_data and recieve_data['totalConvStopSensor'] == 1:
        conv1_motor.run_forever(speed_sp=0)
        conv2_motor.run_forever(speed_sp=0)
        stopper_motor.run_to_abs_pos(speed_sp=100, position_sp=0, stop_action = 'hold')
        stopper_motor.wait_while('running')
        break

    else :
        try:
            conv1_motor.run_forever(speed_sp=recieve_data['eConv1TargetSpeed'])
            conv2_motor.run_forever(speed_sp=-recieve_data['eConv2TargetSpeed'])
            stopper_motor.run_to_abs_pos(speed_sp=recieve_data['eConv2StopperTargetSpeed'], position_sp=recieve_data['eConv2StopperTargetDistance'], stop_action = 'hold')
            
        except:
            print('something is null')
# -----------------------------------------------------------------------

    # sleep
    time.sleep(0.1)
