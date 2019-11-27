import os
import sys
import ev3dev.ev3 as ev3

robot_joint_1_motor = ev3.Motor('outA')
robot_joint_2_motor = ev3.Motor('outB')
robot_hand_motor = ev3.Motor('outC')

# robot_joint_1_motor = ev3.Motor('outA')
# robot_joint_2_motor = ev3.Motor('outB')
# robot_hand_motor = ev3.Motor('outC')


# robot_hand_zero_point = ev3_2.robot_hand_zero_point

# robot_elbow_zero_point = ev3_2.robot_elbow_zero_point

# robot_base_zero_point = ev3_2.robot_base_zero_point



def elbow_ini(robotJoint2TargetSpeed, robot_elbow_zero_point):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point, stop_action = 'hold')
    robot_joint_2_motor.wait_while('running', timeout=5000) # elbow up to ini
def hand_ini(robotHandTargetSpeed, robot_hand_zero_point):
    robot_hand_motor.run_to_abs_pos(speed_sp=robotHandTargetSpeed, position_sp=robot_hand_zero_point, stop_action = 'hold')
    robot_hand_motor.wait_while('running', timeout=5000)    # hand ini
def base_ini(robotJoint1TargetSpeed, robot_base_zero_point):
    robot_joint_1_motor.run_to_abs_pos(speed_sp=robotJoint1TargetSpeed, position_sp=robot_base_zero_point, stop_action = 'hold')
    robot_joint_1_motor.wait_while('running', timeout=15000)    # base ini
def hand_on(robotHandTargetSpeed, robotHandOnTargetDistance, robot_hand_zero_point):
    robot_hand_motor.run_to_abs_pos(speed_sp=robotHandTargetSpeed, position_sp=robot_hand_zero_point + robotHandOnTargetDistance, stop_action = 'hold')
    robot_hand_motor.wait_while('running', timeout=5000) # hand on
def hand_off(robotHandTargetSpeed, robotHandOffTargetDistance, robot_hand_zero_point):
    robot_hand_motor.run_to_abs_pos(speed_sp=robotHandTargetSpeed, position_sp=robot_hand_zero_point + robotHandOffTargetDistance, stop_action = 'hold')
    robot_hand_motor.wait_while('running', timeout=5000) #hand off
def elbow_down_handoff(robotJoint2TargetSpeed, robotJoint2Target2Distance, robot_elbow_zero_point):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point + (robotJoint2Target2Distance), stop_action = 'hold')
    robot_joint_2_motor.wait_while('running', timeout=5000) # elbow down to level2
def elbow_up_to_level3(robotJoint2TargetSpeed, robotJoint2Target3Distance, robot_elbow_zero_point):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point + (robotJoint2Target3Distance), stop_action = 'hold')
    robot_joint_2_motor.wait_while('running', timeout=5000) # elbow up to level3
def elbow_down_to_handon(robotJoint2TargetSpeed, robotJoint2Target1Distance,robot_elbow_zero_point):
    robot_joint_2_motor.run_to_abs_pos(speed_sp=robotJoint2TargetSpeed, position_sp=robot_elbow_zero_point + (robotJoint2Target1Distance), stop_action = 'hold')
    robot_joint_2_motor.wait_while('running', timeout=5000) # elbow down to level1
def base_from_conv_to_test(robotJoint1TargetSpeed, robotJoint1TargetDistance, robot_base_zero_point):
    robot_joint_1_motor.run_to_abs_pos(speed_sp=robotJoint1TargetSpeed, position_sp=robot_base_zero_point + (robotJoint1TargetDistance), stop_action = 'hold')
    robot_joint_1_motor.wait_while('running', timeout=15000) # base move from conv to test
def base_from_test_to_rconv(robotJoint1TargetSpeed, robotJoint1Target2Distance, robot_base_zero_point):
    robot_joint_1_motor.run_to_abs_pos(speed_sp=robotJoint1TargetSpeed, position_sp=robot_base_zero_point + robotJoint1Target2Distance, stop_action = 'hold')
    robot_joint_1_motor.wait_while('running', timeout=15000) # base move from test to rconv


def c_to_t(robotJoint1TargetSpeed , robotJoint1TargetDistance,
robotJoint2TargetSpeed, robotJoint2Target1Distance, robotJoint2Target2Distance, robotJoint2Target3Distance,
robotHandTargetSpeed, robotHandOnTargetDistance, robotHandOffTargetDistance,
robot_hand_zero_point,robot_elbow_zero_point,robot_base_zero_point):
    # elbow_ini(robotJoint2TargetSpeed,robot_elbow_zero_point)
    # hand_ini(robotHandTargetSpeed, robot_hand_zero_point)
    # base_ini(robotJoint1TargetSpeed, robot_base_zero_point)
    hand_off(robotHandTargetSpeed, robotHandOffTargetDistance,robot_hand_zero_point)
    elbow_down_to_handon(robotJoint2TargetSpeed, robotJoint2Target1Distance,robot_elbow_zero_point)
    hand_on(robotHandTargetSpeed, robotHandOnTargetDistance,robot_hand_zero_point)
    elbow_up_to_level3(robotJoint2TargetSpeed, robotJoint2Target3Distance,robot_elbow_zero_point)
    base_from_conv_to_test(robotJoint1TargetSpeed, robotJoint1TargetDistance,robot_base_zero_point)
    elbow_down_handoff(robotJoint2TargetSpeed, robotJoint2Target2Distance,robot_elbow_zero_point)
    hand_off(robotHandTargetSpeed, robotHandOffTargetDistance,robot_hand_zero_point)

    elbow_up_to_level3(robotJoint2TargetSpeed, robotJoint2Target3Distance,robot_elbow_zero_point)
    hand_ini(robotHandTargetSpeed, robot_hand_zero_point)
    base_ini(robotJoint1TargetSpeed, robot_base_zero_point)
    elbow_ini(robotJoint2TargetSpeed,robot_elbow_zero_point)


def t_to_c(robotJoint1TargetSpeed, robotJoint1TargetDistance, robotJoint1Target2Distance,
robotJoint2TargetSpeed, robotJoint2Target1Distance, robotJoint2Target2Distance, robotJoint2Target3Distance,
robotHandTargetSpeed, robotHandOnTargetDistance, robotHandOffTargetDistance,
robot_hand_zero_point,robot_elbow_zero_point,robot_base_zero_point):
    # elbow_ini(robotJoint2TargetSpeed,robot_elbow_zero_point)
    # hand_ini(robotHandTargetSpeed, robot_hand_zero_point)
    # base_ini(robotJoint1TargetSpeed, robot_base_zero_point)

    elbow_up_to_level3(robotJoint2TargetSpeed, robotJoint2Target3Distance,robot_elbow_zero_point)
    base_from_conv_to_test(robotJoint1TargetSpeed, robotJoint1TargetDistance,robot_base_zero_point)
    hand_off(robotHandTargetSpeed, robotHandOffTargetDistance,robot_hand_zero_point)
    elbow_down_to_handon(robotJoint2TargetSpeed, robotJoint2Target1Distance,robot_elbow_zero_point)
    hand_on(robotHandTargetSpeed, robotHandOnTargetDistance,robot_hand_zero_point)
    elbow_up_to_level3(robotJoint2TargetSpeed, robotJoint2Target3Distance,robot_elbow_zero_point)
    base_from_test_to_rconv(robotJoint1TargetSpeed, robotJoint1Target2Distance, robot_base_zero_point)
    elbow_down_handoff(robotJoint2TargetSpeed, robotJoint2Target2Distance,robot_elbow_zero_point)
    hand_off(robotHandTargetSpeed, robotHandOffTargetDistance,robot_hand_zero_point)

    elbow_up_to_level3(robotJoint2TargetSpeed, robotJoint2Target3Distance,robot_elbow_zero_point)
    hand_ini(robotHandTargetSpeed, robot_hand_zero_point)
    base_ini(robotJoint1TargetSpeed, robot_base_zero_point)
    elbow_ini(robotJoint2TargetSpeed,robot_elbow_zero_point)

def ini(robot_elbow_zero_point, robot_hand_zero_point, robot_base_zero_point):

    robot_joint_2_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_elbow_zero_point, stop_action = 'hold')
    robot_joint_2_motor.wait_until_not_moving
    robot_hand_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_hand_zero_point, stop_action = 'hold')
    robot_hand_motor.wait_until_not_moving
    robot_joint_1_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_base_zero_point, stop_action = 'hold')
    robot_joint_1_motor.wait_until_not_moving

def emergency(robot_elbow_zero_point, robot_hand_zero_point, robot_base_zero_point):

    robot_joint_2_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_elbow_zero_point, stop_action = 'hold')
    robot_joint_2_motor.wait_while('running', timeout=5000)
    robot_hand_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_hand_zero_point, stop_action = 'hold')
    robot_hand_motor.wait_while('running', timeout=5000)
    robot_joint_1_motor.run_to_abs_pos(speed_sp=100, position_sp=robot_base_zero_point, stop_action = 'hold')
    robot_joint_1_motor.wait_while('running', timeout=5000)
