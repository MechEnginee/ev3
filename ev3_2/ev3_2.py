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
tM1_sensor = ev3.ColorSensor('in3')
tM2_sensor = ev3.ColorSensor('in2')

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
# robot_joint_1_motor.run_to_abs_pos(speed_sp = 100, position_sp = robot_base_zero_point, stop_action = 'hold')
# robot_joint_1_motor.wait_while('running')
# robot_joint_2_motor.run_to_abs_pos(speed_sp = 100, position_sp = robot_elbow_zero_point - 20, stop_action = 'hold')
# robot_joint_2_motor.wait_while('running')
# robot_hand_motor.run_to_abs_pos(speed_sp = 100, position_sp = robot_hand_zero_point, stop_action = 'hold')
# robot_hand_motor.wait_while('running')
robot_joint_2_motor.run_to_abs_pos(speed_sp = 100, position_sp = robot_elbow_zero_point - 140, stop_action = 'hold')
robot_joint_2_motor.wait_while('running')
#base initialize
robot_joint_1_motor.run_to_abs_pos(speed_sp = 100, position_sp = -30, stop_action = 'hold')
robot_joint_1_motor.wait_while('running')

while True:
    if stopper_sensor.reflected_light_intensity > 3:
        robot_joint_1_motor.stop
        break
    else : 
        robot_joint_1_motor.run_to_abs_pos(speed_sp = 100, position_sp = -150, stop_action = 'hold')
    
robot_base_zero_point = robot_joint_1_motor.position - 20
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
ev3_socket.send(ev3_name.encode('utf-8'))

def elbow_ini(robotJoint2TargetSpeed, robot_elbow_zero_point):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point, stop_action = 'hold')
    robot_joint_2_motor.wait_until_not_moving # elbow up to ini
def hand_ini(robotHandTargetSpeed, robot_hand_zero_point):
    robot_hand_motor.run_to_abs_pos(speed_sp=robotHandTargetSpeed, position_sp=robot_hand_zero_point, stop_action = 'hold')
    robot_hand_motor.wait_until_not_moving    # hand ini
def base_ini(robotJoint1TargetSpeed, robot_base_zero_point):
    robot_joint_1_motor.run_to_abs_pos(speed_sp=robotJoint1TargetSpeed, position_sp=robot_base_zero_point, stop_action = 'hold')
    robot_joint_1_motor.wait_until_not_moving    # base ini
def hand_on(robotHandTargetSpeed, robotHandOnTargetDistance):
    robot_hand_motor.run_to_abs_pos(speed_sp=robotHandTargetSpeed, position_sp=robot_hand_zero_point + robotHandOnTargetDistance, stop_action = 'hold')
    robot_hand_motor.wait_until_not_moving # hand on
def hand_off(robotHandTargetSpeed, robotHandOffTargetDistance):
    robot_hand_motor.run_to_abs_pos(speed_sp=robotHandTargetSpeed, position_sp=robot_hand_zero_point + robotHandOffTargetDistance, stop_action = 'hold')
    robot_hand_motor.wait_until_not_moving #hand off
def elbow_down_handoff(robotJoint2TargetSpeed, robotJoint2Target2Distance):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point + (robotJoint2Target2Distance), stop_action = 'hold')
    robot_joint_2_motor.wait_until_not_moving # elbow down to level2
def elbow_up_to_level3(robotJoint2TargetSpeed, robotJoint2Target3Distance):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point + (robotJoint2Target3Distance), stop_action = 'hold')
    robot_joint_2_motor.wait_until_not_moving # elbow up to level3
def elbow_down_to_handon(robotJoint2TargetSpeed, robotJoint2Target1Distance):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point + (robotJoint2Target1Distance), stop_action = 'hold')
    robot_joint_2_motor.wait_until_not_moving # elbow down to level1
def base_from_conv_to_test(robotJoint1TargetSpeed, robotJoint1TargetDistance):
    robot_joint_1_motor.run_to_abs_pos(speed_sp=robotJoint1TargetSpeed, position_sp=robot_base_zero_point + (robotJoint1TargetDistance), stop_action = 'hold')
    robot_joint_1_motor.wait_until_not_moving # base move from conv to test
def base_from_test_to_rconv(robotJoint1TargetSpeed, robotJoint1Target2Distance):
    robot_joint_1_motor.run_to_abs_pos(speed_sp=robotJoint1TargetSpeed, position_sp=robot_base_zero_point + robotJoint1Target2Distance, stop_action = 'hold')
    robot_joint_1_motor.wait_until_not_moving # base move from test to rconv


def c_to_t(robotJoint1TargetSpeed , robotJoint1TargetDistance,
robotJoint2TargetSpeed, robotJoint2Target1Distance, robotJoint2Target2Distance, robotJoint2Target3Distance,
robotHandTargetSpeed, robotHandOnTargetDistance, robotHandOffTargetDistance):
    elbow_ini(robotJoint2TargetSpeed,robot_elbow_zero_point)
    hand_ini(robotHandTargetSpeed, robot_hand_zero_point)
    base_ini(robotJoint1TargetSpeed, robot_base_zero_point)

    hand_off(robotHandTargetSpeed, robotHandOffTargetDistance)
    elbow_down_to_handon(robotJoint2TargetSpeed, robotJoint2Target1Distance)
    hand_on(robotHandTargetSpeed, robotHandOnTargetDistance)
    elbow_up_to_level3(robotJoint2TargetSpeed, robotJoint2Target3Distance)
    base_from_conv_to_test(robotJoint1TargetSpeed, robotJoint1TargetDistance)
    elbow_down_handoff(robotJoint2TargetSpeed, robotJoint2Target2Distance)
    hand_off(robotHandTargetSpeed, robotHandOffTargetDistance)

    elbow_ini(robotJoint2TargetSpeed,robot_elbow_zero_point)
    hand_ini(robotHandTargetSpeed, robot_hand_zero_point)
    base_ini(robotJoint1TargetSpeed, robot_base_zero_point)


def t_to_c(robotJoint1TargetSpeed, robotJoint1TargetDistance, robotJoint1Target2Distance,
robotJoint2TargetSpeed, robotJoint2Target1Distance, robotJoint2Target2Distance, robotJoint2Target3Distance,
robotHandTargetSpeed, robotHandOnTargetDistance, robotHandOffTargetDistance):

    elbow_ini(robotJoint2TargetSpeed,robot_elbow_zero_point)
    hand_ini(robotHandTargetSpeed, robot_hand_zero_point)
    base_ini(robotJoint1TargetSpeed, robot_base_zero_point)

    elbow_up_to_level3(robotJoint2TargetSpeed, robotJoint2Target3Distance)
    base_from_conv_to_test(robotJoint1TargetSpeed, robotJoint1TargetDistance)
    hand_off(robotHandTargetSpeed, robotHandOffTargetDistance)
    elbow_down_to_handon(robotJoint2TargetSpeed, robotJoint2Target1Distance)
    hand_on(robotHandTargetSpeed, robotHandOnTargetDistance)
    elbow_up_to_level3(robotJoint2TargetSpeed, robotJoint2Target3Distance)
    base_from_test_to_rconv(robotJoint1TargetSpeed, robotJoint1Target2Distance)
    elbow_down_handoff(robotJoint2TargetSpeed, robotJoint2Target2Distance)
    hand_off(robotHandTargetSpeed, robotHandOffTargetDistance)

    elbow_ini(robotJoint2TargetSpeed,robot_elbow_zero_point)
    hand_ini(robotHandTargetSpeed, robot_hand_zero_point)
    base_ini(robotJoint1TargetSpeed, robot_base_zero_point)



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
    send_data['robot_base_zero_point'] = robot_base_zero_point
    send_data['robot_elbow_zero_point'] = robot_elbow_zero_point
    send_data['robot_hand_zero_point'] = robot_hand_zero_point

    # Request
    send_data['request'] = []
    send_data['request'].append('Movename')
    send_data['request'].append('robotJoint1TargetSpeed')
    send_data['request'].append('robotJoint1TargetDistance')
    send_data['request'].append('robotJoint1Target2Distance')
    send_data['request'].append('robotJoint2TargetSpeed')
    send_data['request'].append('robotJoint2Target1Distance')
    send_data['request'].append('robotJoint2Target2Distance')
    send_data['request'].append('robotJoint2Target3Distance')
    send_data['request'].append('robotHandTargetSpeed')
    send_data['request'].append('robotHandOnTargetDistance')
    send_data['request'].append('robotHandOffTargetDistance')


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
    #totalStopMove
    try:
        print(recieve_data)
        if 'Movename' in recieve_data and recieve_data['Movename'] == 'emergency': # emergency situation
            robot_joint_2_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_elbow_zero_point, stop_action = 'hold')
            robot_joint_2_motor.wait_until_not_moving
            robot_hand_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_hand_zero_point, stop_action = 'hold')
            robot_joint_1_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_base_zero_point, stop_action = 'hold')
            robot_joint_1_motor.wait_until_not_moving

        elif 'Movename' in recieve_data and recieve_data['Movename'] == 'c_to_t': # conv to test machine
            print('2')
            c_to_t(recieve_data['robotJoint1TargetSpeed'] , recieve_data['robotJoint1TargetDistance'],
            recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target1Distance'], recieve_data['robotJoint2Target2Distance'], recieve_data['robotJoint2Target3Distance'],
            recieve_data['robotHandTargetSpeed'], recieve_data['robotHandOnTargetDistance'], recieve_data['robotHandOffTargetDistance'])
        
        elif 'Movename' in recieve_data and recieve_data['Movename'] == 't_to_c': # test machine to conv
            print('1')
            t_to_c(recieve_data['robotJoint1TargetSpeed'] , recieve_data['robotJoint1TargetDistance'], recieve_data['robotJoint1Target2Distance'],
            recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target1Distance'], recieve_data['robotJoint2Target2Distance'], recieve_data['robotJoint2Target3Distance'],
            recieve_data['robotHandTargetSpeed'], recieve_data['robotHandOnTargetDistance'], recieve_data['robotHandOffTargetDistance'])

        elif 'Movename' in recieve_data and recieve_data['Movename'] == 'ini': # robot initialize
            robot_joint_2_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_elbow_zero_point, stop_action = 'hold')
            robot_joint_2_motor.wait_until_not_moving
            robot_hand_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_hand_zero_point, stop_action = 'hold')
            robot_hand_motor.wait_until_not_moving
            robot_joint_1_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_base_zero_point, stop_action = 'hold')
            robot_joint_1_motor.wait_until_not_moving
        else:
            print('?')

    except:
        print('something is null')


        
# -----------------------------------------------------------------------

    # sleep
    time.sleep(0.1)
