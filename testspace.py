import socket
import time
import random
import configparser

# import ev3dev.ev3 as ev3
# from ev3dev2.sensor.lego import TouchSensor
# from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4

# Utility Functions
def generate_random_float():
    return random.random()

def generate_random_boolean():
    return random.random() > 0.5


import json
def make_send_data(**kwargs):
    return json.dumps(kwargs)


eConv1EntrySensor = generate_random_boolean()
eConv2EntrySensor = generate_random_boolean()
eConv2StopperSensor = generate_random_boolean()
eConv2TMInputSensor = generate_random_boolean()
    
sensors = dict()
sensors['eConv1EntrySensor'] = eConv1EntrySensor
sensors['eConv2EntrySensor'] = eConv2EntrySensor
sensors['eConv2StopperSensor'] = eConv2StopperSensor
sensors['eConv2TMInputSensor'] = eConv2TMInputSensor

eConv1Speed = generate_random_float()
eConv2Speed = generate_random_float()
eConv2StopperSpeed = generate_random_float()

speeds = dict()
speeds['eConv1Speed'] = eConv1Speed
speeds['eConv2Speed'] = eConv2Speed
speeds['eConv2StopperSpeed'] = eConv2StopperSpeed

send_data = make_send_data(sensors=sensors, speeds=speeds)

print(send_data)
