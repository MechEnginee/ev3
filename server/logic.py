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
            msg = client_socket.recv(1024).decode('utf-8')
            recieved_data = json.loads(msg)

            # 2. Save Data
            save_data(data, recieved_data)

            # 3. Logic
            # -----------------------------------------------------------------------
            # 3.1 Stopper
            if 'eConv2StopperSensor' in data:
                if data['eConv2StopperSensor'] > 2:
                    data['eConv2StopperTargetSpeed'] = read_move('stopper', 'on_speed')
                    data['eConv2StopperTargetDistance'] = read_move('stopper', 'on_dist')
                else:
                    data['eConv2StopperTargetSpeed'] = read_move('stopper', 'off_speed')
                    data['eConv2StopperTargetDistance'] = read_move('stopper', 'off_dist')
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
            client_socket.send(json.dumps(return_data).encode('utf-8'))
    except:
        client_socket.close()


def logic_ev3_2(client_socket, client_addr, data):
    try:
        while True:
            # 1. Recieve
            msg = client_socket.recv(1024).decode('utf-8')
            recieved_data = json.loads(msg)

            # 2. Save Data
            save_data(data, recieved_data)
            
            # 3. Logic
            # -----------------------------------------------------------------------
            # Robot
            # TODO:
            #test machine search
            a = int(data['tM1Sensor'])
            b = int(data['tM2Sensor'])
            c = int(data['tM3Sensor'])
            d = int(data['tM4Sensor'])
            search = [a,b,c,d]
            # search.append(data['tM1Sensor'])
            # search.append(data['tM2Sensor'])
            # search.append(data['tM3Sensor'])
            # search.append(data['tM4Sensor'])
            # print(search)
            for i, value in enumerate(search):
                number = str(i+1)
                
                
                if (data['eConv2StopperSensor'] > 1 and search[i]==0):#검사기에 물체가 있고, test machine 중에 1개라도 비어 있을 때
                    data['Movename'] = 'c_to_t'
                    print(data['Movename'])
                    data['robotJoint1TargetSpeed'] = read_move(('c_to_t'+number), 'motor1_speed')
                    data['robotJoint1TargetDistance'] = read_move(('c_to_t'+number), 'motor1_dist')
                    data['robotJoint2TargetSpeed'] = read_move(('c_to_t'+number), 'motor2_speed')
                    data['robotJoint2Target1Distance'] = read_move(('c_to_t'+number), 'motor2_1_dist')
                    data['robotJoint2Target2Distance'] = read_move(('c_to_t'+number), 'motor2_2_dist')
                    data['robotJoint2Target3Distance'] = read_move(('c_to_t'+number), 'motor2_3_dist')
                    data['robotHandTargetSpeed'] = read_move(('c_to_t'+number), 'motor3_speed')
                    data['robotHandOnTargetDistance'] = read_move(('c_to_t'+number), 'motor3_handon_dist')
                    data['robotHandOffTargetDistance'] = read_move(('c_to_t'+number), 'motor3_handoff_dist')
                    data['robotJoint1Target2Distance'] = 0
                
                elif (data['eConv2StopperSensor'] == 0 and search[i] > 1): #검사기에 물체가 없고, test machine에 1개라도 들어있을 때
                    data['Movename'] = 't_to_c'
                    print(data['Movename'])
                    data['robotJoint1TargetSpeed'] = read_move(('t'+number+'_to_c'), 'motor1_speed')
                    print('1')
                    data['robotJoint1TargetDistance'] = read_move(('t'+number+'_to_c'), 'motor1_dist')
                    print('2')
                    data['robotJoint1Target2Distance'] = read_move(('t'+number+'_to_c'), 'motor1_dist_r')
                    print('3')
                    data['robotJoint2TargetSpeed'] = read_move(('t'+number+'_to_c'), 'motor2_speed')
                    print('4')
                    data['robotJoint2Target1Distance'] = read_move(('t'+number+'_to_c'), 'motor2_1_dist')
                    print('5')
                    data['robotJoint2Target2Distance'] = read_move(('t'+number+'_to_c'), 'motor2_2_dist')
                    print('6')
                    data['robotJoint2Target3Distance'] = read_move(('t'+number+'_to_c'), 'motor2_3_dist')
                    print('7')
                    data['robotHandTargetSpeed'] = read_move(('t'+number+'_to_c'), 'motor3_speed')
                    print('8')
                    data['robotHandOnTargetDistance'] = read_move(('t'+number+'_to_c'), 'motor3_handon_dist')
                    print('9')
                    data['robotHandOffTargetDistance'] = read_move(('t'+number+'_to_c'), 'motor3_handoff_dist')
                    print('10')

            
            if (data['eConv2StopperSensor'] > 1 and data['tM1Sensor']>1 and data['tM2Sensor']>1 and data['tM3Sensor']>1 and data['tM4Sensor']>1):#꽉 차있을 때
                data['Movename'] = 't_to_c'
                print(data['Movename'])
                data['robotJoint1TargetSpeed'] = read_move('t1_to_c', 'motor1_speed')
                data['robotJoint1TargetDistance'] = read_move('t1_to_c', 'motor1_dist')
                data['robotJoint1Target2Distance'] = read_move('t1_to_c', 'motor1_dist_r')
                data['robotJoint2TargetSpeed'] = read_move('t1_to_c', 'motor2_speed')
                data['robotJoint2Target1Distance'] = read_move('t1_to_c', 'motor2_1_dist')
                data['robotJoint2Target2Distance'] = read_move('t1_to_c', 'motor2_2_dist')
                data['robotJoint2Target3Distance'] = read_move('t1_to_c', 'motor2_3_dist')
                data['robotHandTargetSpeed'] = read_move('t1_to_c', 'motor3_speed')
                data['robotHandOnTargetDistance'] = read_move('t1_to_c', 'motor3_handon_dist')
                data['robotHandOffTargetDistance'] = read_move('t1_to_c', 'motor3_handoff_dist')
            
            elif(data['eConv2StopperSensor'] == 0 and data['tM1Sensor'] == 0 and data['tM2Sensor'] == 0 and data['tM3Sensor'] == 0 and data['tM4Sensor'] == 0):# 아예 없는 경우
                data['Movename'] = 'ini'
                print(data['Movename'])
                data['robotJoint1TargetSpeed'] = read_move('robot_off', 'motor1_speed')
                print('1')
                data['robotJoint1TargetDistance'] = data['robot_base_zero_point']
                print('2')
                data['robotJoint2TargetSpeed'] = read_move('robot_off', 'motor2_speed')
                print('3')
                data['robotJoint2Target1Distance'] = read_move('robot_off', 'motor2_speed')
                print('4')
                data['robotJoint2Target2Distance'] = read_move('robot_off', 'motor2_speed')
                print('5')
                data['robotJoint2Target3Distance'] = read_move('robot_off', 'motor2_speed')
                print('6')
                data['robotHandTargetSpeed'] = read_move('robot_off', 'motor3_speed')
                print('7')
                data['robotHandOnTargetDistance'] = read_move('robot_off', 'motor3_dist')
                print('8')
                data['robotHandOffTargetDistance'] = read_move('robot_off', 'motor3_dist')
                print('9')
                data['robotJoint1Target2Distance'] = 0
                print('10')
          
            # Total Stop Button
            if 'totalConvStopSensor' in data and data['totalConvStopSensor'] == 1:
                data['Movename'] = 'emergency'
                print(data['Movename'])
                data['robotJoint1TargetSpeed'] = read_move('robot_off', 'motor1_speed')
                data['robotJoint1TargetDistance'] = data['robot_base_zero_point']
                data['robotJoint2TargetSpeed'] = read_move('robot_off', 'motor2_speed')
                data['robotJoint2Target1Distance'] = read_move('robot_off', 'motor2_speed')
                data['robotJoint2Target2Distance'] = read_move('robot_off', 'motor2_speed')
                data['robotJoint2Target3Distance'] = read_move('robot_off', 'motor2_speed')
                data['robotHandTargetSpeed'] = read_move('robot_off', 'motor3_speed')
                data['robotHandOnTargetDistance'] = read_move('robot_off', 'motor3_dist')
                data['robotHandOffTargetDistance'] = read_move('robot_off', 'motor3_dist')
                data['robotJoint1Target2Distance'] = 0
            
            # -----------------------------------------------------------------------
        
            # 4. Make Return Data
            return_data = make_return_data(data, recieved_data['request'])

            # 5. Send
            client_socket.send(json.dumps(return_data).encode('utf-8'))
    except:
        client_socket.close()


def logic_ev3_3(client_socket, client_addr, data):
    try:
        while True:
            # 1. Recieve
            msg = client_socket.recv(1024).decode('utf-8')
            recieved_data = json.loads(msg)

            # 2. Save Data
            save_data(data, recieved_data)
            #print(data)
            # 3. Logic
            # -----------------------------------------------------------------------
            # data['tM3Sensor']=recieved_data['tM3Sensor']
            # data['tM4Sensor']=recieved_data['tM4Sensor']




            # -----------------------------------------------------------------------

            # 4. Make Return Data
            #return_data = make_return_data(data, recieved_data['request'])

            # 5. Send
            #client_socket.send(json.dumps(return_data).encode('utf-8'))
    except:
        client_socket.close()


def logic_ev3_4(client_socket, client_addr, data):
    try:
        while True:
            # 1. Recieve
            msg = client_socket.recv(1024).decode('utf-8')
            recieved_data = json.loads(msg)

            # 2. Save Data
            save_data(data, recieved_data)
            
            # 3. Logic
            # -----------------------------------------------------------------------
            
            if 'rConv2StopperSensor' in data and (data['rConv2StopperSensor'] > 2):
                data['rConv2StopperTargetSpeed'] = read_move('stopper', 'on_speed')
                data['rConv2StopperTargetDistance'] = read_move('stopper', 'on_dist')
                data['rConv2PushTargetSpeed'] = read_move('push', 'on_speed')
                data['rConv2PushTargetDistance'] = read_move('push', 'on_dist')
            else :
                data['rConv2StopperTargetSpeed'] = read_move('stopper', 'off_speed')
                data['rConv2StopperTargetDistance'] = read_move('stopper', 'off_dist')
                data['rConv2PushTargetSpeed'] = read_move('push', 'off_speed')
                data['rConv2PushTargetDistance'] = read_move('push', 'off_dist')
          
            if 'totalConvStopSensor' in data and (data['totalConvStopSensor'] == 1):
                # Conveyor
                data['rConv1TargetSpeed'] = read_move('conveyor', 'stop_speed')
                data['rConv2TargetSpeed'] = read_move('conveyor', 'stop_speed')
                # Stopper
                data['rConv2StopperTargetSpeed'] = read_move('stopper', 'off_speed')
                data['rConv2StopperTargetDistance'] = read_move('stopper', 'off_dist')
                # Push
                data['rConv2PushTargetSpeed'] = read_move('push', 'off_speed')
                data['rConv2PushTargetDistance'] = read_move('push', 'off_dist')
            else:
                data['rConv1TargetSpeed'] = read_move('conveyor', 'move_speed')
                data['rConv2TargetSpeed'] = read_move('conveyor', 'move_speed')
            print(data)



            # -----------------------------------------------------------------------

            # 4. Make Return Data
            return_data = make_return_data(data, recieved_data['request'])

            # 5. Send
            client_socket.send(json.dumps(return_data).encode('utf-8'))
    except:
        client_socket.close()


def logic_ev3_5(client_socket, client_addr, data):
    try:
        while True:
            # 1. Recieve
            msg = client_socket.recv(1024).decode('utf-8')
            recieved_data = json.loads(msg)

            # 2. Save Data
            save_data(data, recieved_data)
            #print(data)
            # 3. Logic
            # data['rConv2StopperSensor']=recieved_data['rConv2StopperSensor']
            # data['totalConvStopSensor']=recieved_data['totalConvStopSensor']





            # 4. Make Return Data
            #return_data = make_return_data(data, recieved_data['request'])

            # 5. Send
            #client_socket.send(json.dumps(return_data).encode('utf-8'))
    except:
        client_socket.close()
