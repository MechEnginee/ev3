import json
import configparser
import time

def save_data(data, recieved_data):
    for key, value in recieved_data.items():
        if key == 'request':
            pass
        else:
            data[key] = value


def make_return_data(data, request_keys):
    return_data = dict()

    for request_key in request_keys:
        if request_key in data:
            return_data[request_key] = data[request_key]

    return return_data


def read_move(device, value, move_ini_path='move.ini'):
    config = configparser.ConfigParser()
    config.read(move_ini_path)
    return int(config[device][value])


# def log_thread(data):
#     # DB Connection

#     cursor = None

#     while True:

#         econv1speed = data['econv1speed'] if 'econv1speed' in data else None
#         ...
#         # Insert
#         cursor.excute('INSERT INTO TABLE VALUES({}, {}, {}, {}, {}, {})'.format(econv1speed,          ....))
        
        
        
#         time.sleep(0.1)







def logic_ev3_1(client_socket, client_addr, data):
    try:
        while True:
            # 1. Recieve
            msg = client_socket.recv(1024).decode()
            recieved_data = json.loads(msg)

            # 2. Save Data
            save_data(data, recieved_data)

            # 3. Logic
            # -----------------------------------------------------------------------
            # 3.1 Stopper
            if 'eConv2StopperSensor' in data:
                if data['eConv2StopperSensor'] > read_move('stopper', 'threshold'):
                    data['eConv2StopperTargetSpeed'] = read_move('stopper', 'on_speed')
                    data['eConv2StopperTargetDistance'] = read_move('stopper', 'on_dist')
                else:
                    data['eConv2StopperTargetSpeed'] = read_move('stopper', 'off_speed')
                    data['eConv2StopperTargetDistance'] = read_move('stopper', 'off_dist')

            # Total Stop Button
            if 'totalConvStopSensor' in data and data['totalConvStopSensor'] == 1:
                # Conveyor
                data['eConv1TargetSpeed'] = read_move('conveyor', 'stop_speed')
                data['eConv2TargetSpeed'] = read_move('conveyor', 'stop_speed')
                # Stopper
                data['eConv2StopperTargetSpeed'] = read_move('stopper', 'off_speed')
                data['eConv2StopperTargetDistance'] = read_move('stopper', 'off_dist')
            else:
                data['eConv1TargetSpeed'] = read_move('conveyor', 'move_speed')
                data['eConv2TargetSpeed'] = read_move('conveyor', 'move_speed')
            # -----------------------------------------------------------------------

            # 4. Make Return Data
            return_data = make_return_data(data, recieved_data['request'])

            # 5. Send
            client_socket.send(json.dumps(return_data).encode())
    except:
        client_socket.close()


def logic_ev3_2(client_socket, client_addr, data):
    try:
        while True:
            # 1. Recieve
            msg = client_socket.recv(1024).decode()
            recieved_data = json.loads(msg)

            # 2. Save Data
            save_data(data, recieved_data)

            # 3. Logic
            # -----------------------------------------------------------------------
            # Robot
            # TODO:
            #test machine search
            if 'eConv2StopperSensor' in data and 'tM1Sensor' in data and 'tM2Sensor' in data and 'tM3Sensor' in data and 'tM4Sensor' in data:
                search = []
                search.append(data['eConv2StopperSensor'])
                search.append(data['tM1Sensor'])
                search.append(data['tM2Sensor'])
                search.append(data['tM3Sensor'])
                search.append(data['tM4Sensor'])
                if search.index(0)>read_move('stopper', 'threshold') and search.index(1) == 0 and search.index(2) == 0 and search.index(3) == 0 and search.index(4) == 0:#stopper에만 물체 있을 때
                    data['Movename'] = 'c1_to_t1'
                    data['robotJoint1TargetSpeed'] = read_move('c1_to_t1', 'motor1_speed')
                    data['robotJoint1TargetDistance'] = read_move('c1_to_t1', 'motor1_dist')
                    data['robotJoint2TargetSpeed'] = read_move('c1_to_t1', 'motor2_speed')
                    data['robotJoint2Target1Distance'] = read_move('c1_to_t1', 'motor2_1_dist')
                    data['robotJoint2Target2Distance'] = read_move('c1_to_t1', 'motor2_2_dist')
                    data['robotJoint2Target3Distance'] = read_move('c1_to_t1', 'motor2_3_dist')
                    data['robotHandTargetSpeed'] = read_move('c1_to_t1', 'motor3_speed')
                    data['robotHandOnTargetDistance'] = read_move('c1_to_t1', 'motor3_handon_dist')
                    data['robotHandOffTargetDistance'] = read_move('c1_to_t1', 'motor3_handoff_dist')

                    data['robotJoint1TargetDistance'] = data['robot_base_zero_point']
                    data['robotJoint2TargetDistance'] = data['robot_elbow_zero_point']
                    data['robotHandTargetDistance'] = data['robot_hand_zero_point']





            # Total Stop Button
            if 'totalConvStopSensor' in data and data['totalConvStopSensor'] == 1:
                data['TotalStopflag'] = True
                data['robotJoint1TargetDistance'] = data['robot_base_zero_point']
                data['robotJoint1TargetSpeed'] = read_move('robot_off', 'motor1_speed')
                data['robotJoint2TargetDistance'] = data['robot_elbow_zero_point']
                data['robotJoint2TargetSpeed'] = read_move('robot_off', 'motor2_speed')
                data['robotHandTargetDistance'] = data['robot_hand_zero_point']
                data['robotHandTargetSpeed'] = read_move('robot_off', 'motor3_speed')
            # -----------------------------------------------------------------------
                
            # 4. Make Return Data
            return_data = make_return_data(data, recieved_data['request'])

            # 5. Send
            client_socket.send(json.dumps(return_data).encode())
    except:
        client_socket.close()


def logic_ev3_3(client_socket, client_addr, data):
    try:
        while True:
            # 1. Recieve
            msg = client_socket.recv(1024).decode()
            recieved_data = json.loads(msg)

            # 2. Save Data
            save_data(data, recieved_data)

            # 3. Logic
            # -----------------------------------------------------------------------
            




            # -----------------------------------------------------------------------

            # 4. Make Return Data
            return_data = make_return_data(data, recieved_data['request'])

            # 5. Send
            client_socket.send(json.dumps(return_data).encode())
    except:
        client_socket.close()


def logic_ev3_4(client_socket, client_addr, data):
    try:
        while True:
            # 1. Recieve
            msg = client_socket.recv(1024).decode()
            recieved_data = json.loads(msg)

            # 2. Save Data
            save_data(data, recieved_data)

            # 3. Logic
            # -----------------------------------------------------------------------





            # -----------------------------------------------------------------------

            # 4. Make Return Data
            return_data = make_return_data(data, recieved_data['request'])

            # 5. Send
            client_socket.send(json.dumps(return_data).encode())
    except:
        client_socket.close()


def logic_ev3_5(client_socket, client_addr, data):
    try:
        while True:
            # 1. Recieve
            msg = client_socket.recv(1024).decode()
            recieved_data = json.loads(msg)

            # 2. Save Data
            save_data(data, recieved_data)

            # 3. Logic






            # 4. Make Return Data
            return_data = make_return_data(data, recieved_data['request'])

            # 5. Send
            client_socket.send(json.dumps(return_data).encode())
    except:
        client_socket.close()
