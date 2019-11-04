import socket
import time
import random
import configparser
import json
import struct
import datetime

# import ev3dev.ev3 as ev3
# from ev3dev2.sensor.lego import TouchSensor
# from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4

# Utility Functions
# -----------------------------------------------------------------------
def int_to_bytes(v):
    return v.to_bytes(4, 'big')

def float_to_bytes(v):
    return struct.pack('!f', v)

def bool_to_bytes(b):
    return b.to_bytes(1, 'big')

def bytes_to_int(b):
    return int.from_bytes(b, 'big')

def bytes_to_float(b):
    return struct.unpack('!f', b)[0]

def bytes_to_bool(b):
    return bool.from_bytes(b, 'big')


def generate_random_float():
    return random.random()

def generate_random_boolean():
    return random.random() > 0.5

def load_config(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)
    return config['config']['ip'].replace('"', ''), int(config['config']['port']), int(config['config']['size'])


def parse_data_ev3_1(data):
    eConv1EntrySensor = bytes_to_bool(data[0:1])
    eConv2EntrySensor = bytes_to_bool(data[1:2])
    eConv2StopperSensor = bytes_to_bool(data[2:3])
    eConv2TMInputSensor = bytes_to_bool(data[3:4])

    eConv1Speed = bytes_to_float(data[4:8])
    eConv2Speed = bytes_to_float(data[8:12])
    eConv2StopperSpeed = bytes_to_float(data[12:16])

    return eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, eConv2TMInputSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed


def write_data_ev3_1(eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, eConv2TMInputSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed):
    data = bytes()

    data += bool_to_bytes(eConv1EntrySensor)
    data += bool_to_bytes(eConv2EntrySensor)
    data += bool_to_bytes(eConv2StopperSensor)
    data += bool_to_bytes(eConv2TMInputSensor)

    data += float_to_bytes(eConv1Speed)
    data += float_to_bytes(eConv2Speed)
    data += float_to_bytes(eConv2StopperSpeed)

    return data
# -----------------------------------------------------------------------

# ev3 Setting
# Motor
# motor_conv1 = ev3.LargeMotor(ev3.OUTPUT_A)
# motor_conv2 = ev3.LargeMotor(ev3.OUTPUT_B)
# motor_conv2_stopper = ev3.LargeMotor(ev3.OUTPUT_C)

# Sensor
# sensor_conv1_entry = TouchSensor(ev3.INPUT_1)
# sensor_conv2_entry = TouchSensor(ev3.INPUT_2)
# sensor_conv2_stopper = TouchSensor(ev3.INPUT_3)
# sensor_conv2_tm = TouchSensor(ev3.INPUT_4)


# Socket Setting
ip, port, size = load_config('ev3_1.ini')
address = (ip, port)

# Connecting
ev3_1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ev3_1_socket.connect(address)



while True:
    # Get Sensor Values
    # TODO: Sensors @TJ
    # eConv1EntrySensor = sensor_conv1_entry.is_pressed
    # eConv2EntrySensor = sensor_conv2_entry.is_pressed
    # eConv2StopperSensor = sensor_conv2_stopper.is_pressed
    # eConv2TMInputSensor = sensor_conv2_tm.is_pressed

    eConv1EntrySensor = generate_random_boolean()
    eConv2EntrySensor = generate_random_boolean()
    eConv2StopperSensor = generate_random_boolean()
    eConv2TMInputSensor = generate_random_boolean()

    # Get Motor Speed
    # TODO: Get Motor Speed @TJ
    # eConv1Speed = ????
    # eConv2Speed = ????
    # eConv2StopperSpeed = ????

    eConv1Speed = generate_random_float()
    eConv2Speed = generate_random_float()
    eConv2StopperSpeed = generate_random_float()

    # Make Send Data
    data = write_data_ev3_1(eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, eConv2TMInputSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed)

    # Send Data
    ev3_1_socket.send(data)

    # Recieve Data
    data = ev3_1_socket.recv(size)
    eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, eConv2TMInputSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed = parse_data_ev3_1(data)
    print('{} eConv1EntrySensor-{}, eConv2EntrySensor-{}, eConv2StopperSensor-{}, eConv2TMInputSensor-{}, eConv1Speed-{}, eConv2Speed-{}, eConv2StopperSpeed-{}'.format(
        datetime.datetime.now(), eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, eConv2TMInputSensor, eConv1Speed, eConv2Speed, eConv2StopperSpeed
    ))

    # TODO: Move Motor @TJ

    # sleep
    time.sleep(0.1)
