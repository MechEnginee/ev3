import socket
import time
import random
import configparser
import json

# import ev3dev.ev3 as ev3
# from ev3dev2.sensor.lego import TouchSensor
# from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4

# Utility Functions
def generate_random_float():
    return random.random()

def generate_random_boolean():
    return random.random() > 0.5


def load_ip_port(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)
    return config['config']['ip'].replace('"', ''), int(config['config']['port']), int(config['config']['size'])

def make_send_data(**kwargs):
    return json.dumps(kwargs)

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
ip, port, size = load_ip_port('ev3_1.ini')
address = (ip, port)

# Connecting
# TODO: Socket 연결 실패하면 어떻게 해야 하는지? -> 일정 횟수 시도 후 실패 메세지
ev3_1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ev3_1_socket.connect(address)



while True:
    # Get Sensor Values
    # TODO: 센서 값 받아오는 코드 작성
    # eConv1EntrySensor = sensor_conv1_entry.is_pressed
    # eConv2EntrySensor = sensor_conv2_entry.is_pressed
    # eConv2StopperSensor = sensor_conv2_stopper.is_pressed
    # eConv2TMInputSensor = sensor_conv2_tm.is_pressed

    eConv1EntrySensor = generate_random_boolean()
    eConv2EntrySensor = generate_random_boolean()
    eConv2StopperSensor = generate_random_boolean()
    eConv2TMInputSensor = generate_random_boolean()
    
    sensors = dict()
    sensors['eConv1EntrySensor'] = eConv1EntrySensor
    sensors['eConv2EntrySensor'] = eConv2EntrySensor
    sensors['eConv2StopperSensor'] = eConv2StopperSensor
    sensors['eConv2TMInputSensor'] = eConv2TMInputSensor


    # Get Motor Speed
    # TODO: Motor Speed 받아오는 코드 작성
    # eConv1Speed = ????
    # eConv2Speed = ????
    # eConv2StopperSpeed = ????

    eConv1Speed = generate_random_float()
    eConv2Speed = generate_random_float()
    eConv2StopperSpeed = generate_random_float()
    
    speeds = dict()
    speeds['eConv1Speed'] = eConv1Speed
    speeds['eConv2Speed'] = eConv2Speed
    speeds['eConv2StopperSpeed'] = eConv2StopperSpeed

    # Make Send Data
    send_data = make_send_data(sensors=sensors, speeds=speeds)

    # Send Data
    ev3_1_socket.send(send_data.encode())

    # Recieve Data
    msg = ev3_1_socket.recv(size).decode()
    print("[{}] message : {}".format(ev3_1_socket,msg))

    # TODO: 행동 실행 @박태진사원

    # sleep
    time.sleep(0.1)
