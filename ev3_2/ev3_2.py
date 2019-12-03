import os
import sys
import socket
import time
import configparser
import json
import struct
import datetime
import ev3dev.ev3 as ev3
import threading

robot_base_zero_point = 0
robot_elbow_zero_point = 0
robot_hand_zero_point = 0
switch = False
Flag = False
# Utility Functions
def load_config(ini_path):
    config = configparser.ConfigParser()
    config.read(ini_path)
    return config['config']['ip'], int(config['config']['port'])

# ev3 Setting
# -----------------------------------------------------------------------
# Sensor

# tM1_sensor = ev3.ColorSensor('in3')
# tM2_sensor = ev3.ColorSensor('in2')
# stopper_sensor = ev3.ColorSensor('in1')

# Motor
robot_joint_1_motor = ev3.Motor('outA')
robot_joint_2_motor = ev3.Motor('outB')
robot_hand_motor = ev3.Motor('outC')

# ev3 Name
ev3_name = 'ev3_2'

# -----------------------------------------------------------------------

def find_elbow_hand_zero_location():
    #elbow initialize
    robot_joint_2_motor.run_to_abs_pos(speed_sp=100, position_sp=-300, stop_action = 'hold')
    robot_joint_2_motor.wait_until('stalled')
    robot_elbow_zero_point = robot_joint_2_motor.position + 60
    robot_joint_2_motor.run_to_abs_pos(speed_sp=50, position_sp=robot_elbow_zero_point+40, stop_action = 'hold')
    robot_joint_2_motor.wait_while('running')
    #hand initialize
    robot_hand_motor.run_to_abs_pos(speed_sp=100, position_sp=300, stop_action = 'hold')
    robot_hand_motor.wait_until('stalled')
    robot_hand_zero_point = robot_hand_motor.position - 40
    robot_hand_motor.run_to_abs_pos(speed_sp=50, position_sp=robot_hand_zero_point, stop_action = 'hold')
    robot_hand_motor.wait_while('running')
    robot_joint_1_motor.run_to_abs_pos(speed_sp=100, position_sp=60, stop_action = 'hold')
    robot_joint_1_motor.wait_while('running')
    return robot_elbow_zero_point, robot_hand_zero_point

def find_base_zero_point(stopper_sensor_data):
    robot_base_zero_point = 0
    if stopper_sensor_data == 1:
        robot_joint_1_motor.stop
        robot_joint_1_motor.wait_until_not_moving
        robot_base_zero_point = robot_joint_1_motor.position + 10
        robot_joint_2_motor.run_to_abs_pos(speed_sp=50, position_sp=robot_elbow_zero_point, stop_action = 'hold')
        robot_joint_2_motor.wait_while('running')

    else : 
        robot_joint_1_motor.run_to_abs_pos(speed_sp = 100, position_sp = -50, stop_action = 'hold')

    return robot_base_zero_point


# Socket Setting
ip, port = load_config(ev3_name + '.ini')
address = (ip, port)

# Connecting
ev3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ev3_socket.connect(address)
ev3_socket.send(ev3_name.encode('utf-8'))

# elbow, hand setting
robot_elbow_zero_point, robot_hand_zero_point = find_elbow_hand_zero_location()

# base setting
while robot_base_zero_point==0:
    send_data = dict()
    send_data['robotJoint1Speed'] = robot_joint_1_motor.speed
    send_data['robotJoint2Speed'] = robot_joint_2_motor.speed
    send_data['robotHandSpeed'] = robot_hand_motor.speed
    send_data['request'] = []
    send_data['request'].append('eConv2StopperSensor')
    send_msg = json.dumps(send_data)
    # Send Data
    try:
        send_msg = json.dumps(send_data)
        ev3_socket.send(send_msg.encode('utf-8'))
    except:
        print ('Encoding JSON has failed')
        
    
    # Recieve Data
    try:
        recieve_msg = ev3_socket.recv(1024).decode('utf-8')
        recieve_data = json.loads(recieve_msg)
    except:
        print ('Decoding JSON has failed')
        

    robot_base_zero_point = find_base_zero_point(recieve_data['eConv2StopperSensor'])

    time.sleep(0.1)

print(robot_elbow_zero_point, robot_hand_zero_point, robot_base_zero_point)

def elbow_ini(robotJoint2TargetSpeed, robot_elbow_zero_point):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point, stop_action = 'hold')
    robot_joint_2_motor.wait_while('running') # elbow up to ini
def hand_ini(robotHandTargetSpeed, robot_hand_zero_point):
    robot_hand_motor.run_to_abs_pos(speed_sp=robotHandTargetSpeed, position_sp=robot_hand_zero_point, stop_action = 'hold')
    robot_hand_motor.wait_while('running')    # hand ini
def base_ini(robotJoint1TargetSpeed, robot_base_zero_point):
    robot_joint_1_motor.run_to_abs_pos(speed_sp=robotJoint1TargetSpeed, position_sp=robot_base_zero_point, stop_action = 'hold')
    robot_joint_1_motor.wait_while('running')    # base ini
def hand_on(robotHandTargetSpeed, robotHandOnTargetDistance, robot_hand_zero_point):
    robot_hand_motor.run_to_abs_pos(speed_sp=robotHandTargetSpeed, position_sp=robot_hand_zero_point + robotHandOnTargetDistance, stop_action = 'hold')
    robot_hand_motor.wait_while('running') # hand on
def hand_off(robotHandTargetSpeed, robotHandOffTargetDistance, robot_hand_zero_point):
    robot_hand_motor.run_to_abs_pos(speed_sp=robotHandTargetSpeed, position_sp=robot_hand_zero_point + robotHandOffTargetDistance, stop_action = 'hold')
    robot_hand_motor.wait_while('running') #hand off
def elbow_down_handoff(robotJoint2TargetSpeed, robotJoint2Target2Distance, robot_elbow_zero_point):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point + (robotJoint2Target2Distance), stop_action = 'hold')
    robot_joint_2_motor.wait_while('running') # elbow down to level2
def elbow_up_to_level3(robotJoint2TargetSpeed, robotJoint2Target3Distance, robot_elbow_zero_point):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point + (robotJoint2Target3Distance), stop_action = 'hold')
    robot_joint_2_motor.wait_while('running', timeout=3000) # elbow up to level3
def elbow_down_to_handon(robotJoint2TargetSpeed, robotJoint2Target1Distance,robot_elbow_zero_point):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point + (robotJoint2Target1Distance), stop_action = 'hold')
    robot_joint_2_motor.wait_while('running') # elbow down to level1
def base_from_conv_to_test(robotJoint1TargetSpeed, robotJoint1TargetDistance, robot_base_zero_point):
    robot_joint_1_motor.run_to_abs_pos(speed_sp=robotJoint1TargetSpeed, position_sp=robot_base_zero_point + (robotJoint1TargetDistance), stop_action = 'hold')
    robot_joint_1_motor.wait_while('running', timeout=6000) # base move from conv to test
def base_from_test_to_rconv(robotJoint1TargetSpeed, robotJoint1Target2Distance, robot_base_zero_point):
    robot_joint_1_motor.run_to_abs_pos(speed_sp=robotJoint1TargetSpeed, position_sp=robot_base_zero_point + robotJoint1Target2Distance, stop_action = 'hold')
    robot_joint_1_motor.wait_while('running') # base move from test to rconv


def c_to_t(recieve_data):
    # elbow_ini(robotJoint2TargetSpeed,robot_elbow_zero_point)
    # hand_ini(robotHandTargetSpeed, robot_hand_zero_point)
    # base_ini(robotJoint1TargetSpeed, robot_base_zero_point)
    hand_off(recieve_data['robotHandTargetSpeed'], recieve_data['robotHandOffTargetDistance'], robot_hand_zero_point)
    elbow_down_to_handon(recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target1Distance'], robot_elbow_zero_point)
    hand_on(recieve_data['robotHandTargetSpeed'], recieve_data['robotHandOnTargetDistance'], robot_hand_zero_point)
    elbow_up_to_level3(recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target3Distance'], robot_elbow_zero_point)
    base_from_conv_to_test(recieve_data['robotJoint1TargetSpeed'], recieve_data['robotJoint1TargetDistance'], robot_base_zero_point)
    elbow_down_handoff(recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target2Distance'], robot_elbow_zero_point)
    hand_off(recieve_data['robotHandTargetSpeed'], recieve_data['robotHandOffTargetDistance'], robot_hand_zero_point)

    elbow_up_to_level3(recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target3Distance'], robot_elbow_zero_point)
    hand_ini(recieve_data['robotHandTargetSpeed'], robot_hand_zero_point)
    # base_ini(recieve_data['robotJoint1TargetSpeed'], robot_base_zero_point)
    elbow_ini(recieve_data['robotJoint2TargetSpeed'],robot_elbow_zero_point)
    global switch
    switch = False
    global Flag
    Flag = False

def t_to_c(recieve_data):
    # elbow_ini(robotJoint2TargetSpeed,robot_elbow_zero_point)
    # hand_ini(robotHandTargetSpeed, robot_hand_zero_point)
    # base_ini(robotJoint1TargetSpeed, robot_base_zero_point)

    elbow_up_to_level3(recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target3Distance'], robot_elbow_zero_point)
    base_from_conv_to_test(recieve_data['robotJoint1TargetSpeed'], recieve_data['robotJoint1TargetDistance'],robot_base_zero_point)
    hand_off(recieve_data['robotHandTargetSpeed'], recieve_data['robotHandOffTargetDistance'],robot_hand_zero_point)
    elbow_down_to_handon(recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target1Distance'],robot_elbow_zero_point)
    hand_on(recieve_data['robotHandTargetSpeed'], recieve_data['robotHandOnTargetDistance'],robot_hand_zero_point)
    elbow_up_to_level3(recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target3Distance'],robot_elbow_zero_point)
    base_from_test_to_rconv(recieve_data['robotJoint1TargetSpeed'], recieve_data['robotJoint1Target2Distance'], robot_base_zero_point)
    elbow_down_handoff(recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target2Distance'], robot_elbow_zero_point)
    hand_off(recieve_data['robotHandTargetSpeed'], recieve_data['robotHandOffTargetDistance'], robot_hand_zero_point)

    elbow_up_to_level3(recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target3Distance'], robot_elbow_zero_point)
    hand_ini(recieve_data['robotHandTargetSpeed'], robot_hand_zero_point)
    # base_ini(recieve_data['robotJoint1TargetSpeed'], robot_base_zero_point)
    elbow_ini(recieve_data['robotJoint2TargetSpeed'], robot_elbow_zero_point)
    global switch
    switch = False
    global Flag
    Flag = False

def ini(robot_elbow_zero_point, robot_hand_zero_point, robot_base_zero_point):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_elbow_zero_point, stop_action = 'hold')
    robot_joint_2_motor.wait_until_not_moving
    robot_hand_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_hand_zero_point, stop_action = 'hold')
    robot_hand_motor.wait_until_not_moving
    robot_joint_1_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_base_zero_point, stop_action = 'hold')
    robot_joint_1_motor.wait_until_not_moving
    global Flag
    Flag = True




def emergency(robot_elbow_zero_point, robot_hand_zero_point, robot_base_zero_point):

    robot_joint_2_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_elbow_zero_point, stop_action = 'hold')
    robot_joint_2_motor.wait_while('running')
    robot_hand_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_hand_zero_point, stop_action = 'hold')
    robot_hand_motor.wait_while('running')
    robot_joint_1_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_base_zero_point, stop_action = 'hold')
    robot_joint_1_motor.wait_while('running')
    global switch
    switch = False



while True:
    send_data = dict()

# -----------------------------------------------------------------------
    # Get Sensor Values
    # send_data['eConv2StopperSensor'] = stopper_sensor.reflected_light_intensity
    # send_data['tM1Sensor'] = tM1_sensor.reflected_light_intensity
    # send_data['tM2Sensor'] = tM2_sensor.reflected_light_intensity

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
    try:
        # Make Send Data
        send_msg = json.dumps(send_data)
        # Send Data
        ev3_socket.send(send_msg.encode('utf-8'))

    except ValueError:
        print ('Encoding JSON has failed')
        
    # Recieve Data
    try:
        recieve_msg = ev3_socket.recv(1024).decode('utf-8')
        recieve_data = json.loads(recieve_msg)
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print ('Decoding JSON has failed')

    # Move
# -----------------------------------------------------------------------
    if switch == False:
        #try:
        if 'Movename' in recieve_data and recieve_data['Movename'] == 'emergency': # emergency situation
            print(recieve_data['Movename'])
            emergency = threading.Thread(target=emergency, args=(robot_elbow_zero_point, robot_hand_zero_point, robot_base_zero_point,))
            emergency.start()
            emergency.join()
            break

        elif 'Movename' in recieve_data and recieve_data['Movename'] == 'c_to_t': # conv to test machine
            print(recieve_data['Movename'])
            ctot = threading.Thread(target=c_to_t, args=(recieve_data,))
            ctot.start()
            switch = True
            # robotarm.c_to_t(recieve_data['robotJoint1TargetSpeed'] , recieve_data['robotJoint1TargetDistance'],
            # recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target1Distance'], recieve_data['robotJoint2Target2Distance'], recieve_data['robotJoint2Target3Distance'],
            # recieve_data['robotHandTargetSpeed'], recieve_data['robotHandOnTargetDistance'], recieve_data['robotHandOffTargetDistance'],
            # robot_hand_zero_point,robot_elbow_zero_point,robot_base_zero_point)
        
        elif 'Movename' in recieve_data and recieve_data['Movename'] == 't_to_c': # test machine to conv
            print(recieve_data['Movename'])
            ttoc = threading.Thread(target=t_to_c, args=(recieve_data,))
            ttoc.start()
            switch = True
            # robotarm.t_to_c(recieve_data['robotJoint1TargetSpeed'] , recieve_data['robotJoint1TargetDistance'], recieve_data['robotJoint1Target2Distance'],
            # recieve_data['robotJoint2TargetSpeed'], recieve_data['robotJoint2Target1Distance'], recieve_data['robotJoint2Target2Distance'], recieve_data['robotJoint2Target3Distance'],
            # recieve_data['robotHandTargetSpeed'], recieve_data['robotHandOnTargetDistance'], recieve_data['robotHandOffTargetDistance'],
            # robot_hand_zero_point,robot_elbow_zero_point,robot_base_zero_point)

        elif 'Movename' in recieve_data and recieve_data['Movename'] == 'ini': # robot initialize
            print(recieve_data['Movename'])
            if Flag is False:
                ini(robot_elbow_zero_point, robot_hand_zero_point, robot_base_zero_point)
                
            else :
                pass

            # ini = threading.Thread(target=ini, args=(robot_elbow_zero_point, robot_hand_zero_point, robot_base_zero_point,))
            # ini.start()
            # ini.join()

        #except:
            # print('something is none')

        
   
# -----------------------------------------------------------------------

    # sleep
    time.sleep(0.1)
