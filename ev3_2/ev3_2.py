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
stopper_sensor = ev3.ColorSensor('in1')
tM1_sensor = ev3.ColorSensor('in2')
tM2_sensor = ev3.ColorSensor('in3')

# Motor
robot_joint_1_motor = ev3.Motor('outA')
robot_joint_2_motor = ev3.Motor('outB')
robot_hand_motor = ev3.Motor('outC')

# ev3 Name
ev3_name = 'ev3_2'

# #robot initialize
robot_base_zero_point = 0
robot_elbow_zero_point = 0
robot_hand_zero_point = 0
robot_joint_1_motor.run_to_abs_pos(speed_sp = 100, position_sp = robot_base_zero_point, stop_action = 'hold')
robot_joint_2_motor.run_to_abs_pos(speed_sp = 100, position_sp = robot_elbow_zero_point, stop_action = 'hold')
robot_hand_motor.run_to_abs_pos(speed_sp = 100, position_sp = robot_hand_zero_point, stop_action = 'hold')
robot_joint_1_motor.wait_while('running')
robot_joint_2_motor.wait_while('running')
robot_hand_motor.wait_while('running')

#base initialize
robot_joint_1_motor.run_to_abs_pos(speed_sp = 100, position_sp = 50, stop_action = 'hold')
robot_joint_1_motor.wait_while('running')
while True:
    if stopper_sensor.reflected_light_intensity > 0.5:
        robot_joint_1_motor.stop
        break
    else : 
        robot_joint_1_motor.run_to_abs_pos(speed_sp = 100, position_sp = -100, stop_action = 'hold')
    
robot_base_zero_point = robot_joint_1_motor.position
robot_joint_1_motor.run_to_abs_pos(speed_sp = 50, position_sp=robot_base_zero_point, stop_action = 'hold')
robot_joint_1_motor.wait_while('running')

#elbow initialize
robot_joint_2_motor.run_to_abs_pos(speed_sp=100, position_sp=-300, stop_action = 'hold')
robot_joint_2_motor.wait_until('stalled')
robot_elbow_zero_point = robot_joint_2_motor.position + 70
robot_joint_2_motor.run_to_abs_pos(speed_sp=50, position_sp=robot_elbow_zero_point, stop_action = 'hold')
robot_joint_2_motor.wait_while('running')
#hand initialize
robot_hand_motor.run_to_abs_pos(speed_sp=100, position_sp=300, stop_action = 'hold')
robot_hand_motor.wait_until('stalled')
robot_hand_zero_point = robot_hand_motor.position - 40
robot_hand_motor.run_to_abs_pos(speed_sp=50, position_sp=robot_hand_zero_point, stop_action = 'hold')
robot_hand_motor.wait_while('running')
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
    send_data['eConv2StopperSensor'] = stopper_sensor.reflected_light_intensity
    send_data['tM1Sensor'] = tM1_sensor.reflected_light_intensity
    send_data['tM2Sensor'] = tM2_sensor.reflected_light_intensity

    # Get Motor Speed
    send_data['robotJoint1Speed'] = robot_joint_1_motor.speed
    send_data['robotJoint2Speed'] = robot_joint_2_motor.speed
    send_data['robotHandSpeed'] = robot_hand_motor.speed

    # Request
    send_data['request'] = []
    send_data['request'].append('robotJoint1TargetSpeed')
    send_data['request'].append('robotJoint1TargetDistance')
    send_data['request'].append('robotJoint2TargetSpeed')
    send_data['request'].append('robotJoint2TargetDistance')
    send_data['request'].append('robotHandTargetSpeed')
    send_data['request'].append('robotHandTargetDistance')
# -----------------------------------------------------------------------

    # Make Send Data
    send_msg = json.dumps(send_data)

    # Send Data
    ev3_socket.send(send_msg.encode())

    # Recieve Data
    recieve_msg = ev3_socket.recv(1024).decode()
    recieve_data = json.loads(recieve_msg)

    # Move
# -----------------------------------------------------------------------
    if 'robotJoint1TargetSpeed' in recieve_data and 'robotJoint1TargetDistance' in recieve_data:
        robot_joint_1_motor.run_to_abs_pos(speed_sp=recieve_data['robotJoint1TargetSpeed'], position_sp=recieve_data['robotJoint1TargetDistance'], stop_action = 'hold')
    
    if 'robotJoint2TargetSpeed' in recieve_data and 'robotJoint2TargetDistance' in recieve_data:
        robot_joint_2_motor.run_to_abs_pos(speed_sp=recieve_data['robotJoint2TargetSpeed'], position_sp=recieve_data['robotJoint2TargetDistance'], stop_action = 'hold')
    
    if 'robotHandTargetSpeed' in recieve_data and 'robotHandTargetDistance' in recieve_data:
        robot_hand_motor.run_to_abs_pos(speed_sp=recieve_data['robotHandTargetSpeed'], position_sp=recieve_data['robotHandTargetDistance'], stop_action = 'hold')
# -----------------------------------------------------------------------

    # sleep
    time.sleep(0.1)
