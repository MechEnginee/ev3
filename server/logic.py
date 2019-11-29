import json
import configparser
import time
import sqlite3

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
        else:
            return_data[request_key] = 0

    return return_data


def read_move(device, value, move_ini_path='move.ini'):
    config = configparser.ConfigParser()
    config.read(move_ini_path)
    return int(config[device][value])

def search_test_machine_1(tM1,tM2,tM3,tM4):#비어있는 test machine기 탐색
    search =[tM1,tM2,tM3,tM4]
    Trigger = True
    number = 1

    for i, value in enumerate(search):
        if(value==0):
            Trigger = False
            number = str(i+1)
            break
    

    return number, Trigger

def search_test_machine_2(tM1,tM2,tM3,tM4):#차있는 test machine기 탐색
    search =[tM1,tM2,tM3,tM4]
    Trigger = True
    number = 1

    for i, value in enumerate(search):
        if(value>1):
            Trigger = False
            number = str(i+1)
            break
    

    return number, Trigger


def log_thread(data):

    # SQL 쿼리 실행
    # cursor.execute("CREATE TABLE EV3_Sensor(eConv1EntrySensor int, eConv2EntrySensor float, eConv2StopperSensor int, tM1Sensor int, tM2Sensor int, tM3Sensor int, tM4Sensor int,rConv1EntrySensor float,rConv2EntrySensor float,rConv2StopperSensor int)")
    # conn.commit()
    # cursor.execute("CREATE TABLE EV3_Motor(eConv1Speed float, eConv2Speed float, eConv2StopperSpeed float, robotJoint1Speed float, robotJoint2Speed float, robotHandSpeed float, rConv1Speed float,rConv2Speed float,rConv2StopperSpeed float,rConv2PushSpeed float)")
    # conn.commit()
    while True:
        # try:
            # Sqlite DB Connection
            conn = sqlite3.connect("C:/Users/TJ/ev3/server/ev3dev.db")
            # Connection 으로부터 Cursor 생성
            cursor = conn.cursor()
            # while True:
            #ev3_1
            eConv1EntrySensor = data['eConv1EntrySensor'] if 'eConv1EntrySensor' in data else None
            eConv2EntrySensor = data['eConv2EntrySensor'] if 'eConv2EntrySensor' in data else None
            tM1Sensor = data['tM1Sensor'] if 'tM1Sensor' in data else None
            tM2Sensor = data['tM2Sensor'] if 'tM2Sensor' in data else None
            eConv1Speed = data['eConv1Speed'] if 'eConv1Speed' in data else None
            eConv2Speed = data['eConv2Speed'] if 'eConv2Speed' in data else None
            eConv2StopperSpeed = data['eConv2StopperSpeed'] if 'eConv2StopperSpeed' in data else None
            #ev3_2
            robotJoint1Speed = data['robotJoint1Speed'] if 'robotJoint1Speed' in data else None
            robotJoint2Speed = data['robotJoint2Speed'] if 'robotJoint2Speed' in data else None
            robotHandSpeed = data['robotHandSpeed'] if 'robotHandSpeed' in data else None
            #ev3_3
            eConv2StopperSensor = data['eConv2StopperSensor']  if 'eConv2StopperSensor' in data else None
            tM3Sensor = data['tM3Sensor'] if 'tM3Sensor' in data else None
            tM4Sensor = data['tM4Sensor'] if 'tM4Sensor' in data else None
            #ev3_4
            rConv1EntrySensor = data['rConv1EntrySensor'] if 'rConv1EntrySensor' in data else None
            rConv2EntrySensor = data['rConv2EntrySensor'] if 'rConv2EntrySensor' in data else None
            rConv1Speed = data['rConv1Speed'] if 'rConv1Speed' in data else None
            rConv2Speed = data['rConv2Speed'] if 'rConv2Speed' in data else None
            rConv2StopperSpeed = data['rConv2StopperSpeed'] if 'rConv2StopperSpeed' in data else None
            rConv2PushSpeed = data['rConv2PushSpeed'] if 'rConv2PushSpeed' in data else None
            #ev3_5
            rConv2StopperSensor = data['rConv2StopperSensor'] if 'rConv2StopperSensor' in data else None
            totalConvStopSensor = data['totalConvStopSensor'] if 'totalConvStopSensor' in data else None

            # Insert
            cursor.execute("INSERT INTO EV3DEV VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, tM1Sensor, tM2Sensor, tM3Sensor, tM4Sensor,rConv1EntrySensor,rConv2EntrySensor,rConv2StopperSensor,eConv1Speed, eConv2Speed, eConv2StopperSpeed, robotJoint1Speed, robotJoint2Speed, robotHandSpeed, rConv1Speed, rConv2Speed, rConv2StopperSpeed, rConv2PushSpeed))
            conn.commit()
            # cursor.execute("INSERT INTO EV3_Motor VALUES(?,?,?,?,?,?,?,?,?,?)",(eConv1Speed, eConv2Speed, eConv2StopperSpeed, robotJoint1Speed, robotJoint2Speed, robotHandSpeed, rConv1Speed, rConv2Speed, rConv2StopperSpeed, rConv2PushSpeed))
            # conn.commit()
            
            conn.close()
            time.sleep(0.1)
        # except:
            # print('db problem')
    


    
    
    


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
                if data['eConv2StopperSensor'] > 1:
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
            #test machine search


            #print(data)


            if len(recieved_data['request']) == 1:
                # 4. Make Return Data
                return_data = make_return_data(data, recieved_data['request'])
                # 5. Send
                client_socket.send(json.dumps(return_data).encode('utf-8'))
                
            else:
                tM1 = int(data['tM1Sensor'])
                tM2 = int(data['tM2Sensor'])
                tM3 = int(data['tM3Sensor'])
                tM4 = int(data['tM4Sensor'])
                if('eConv2StopperSensor' in data and data['eConv2StopperSensor'] > 1):
                    number , Trigger = search_test_machine_1(tM1,tM2,tM3,tM4)
                    if (Trigger is False): #물체가 있고, test machine 중에 1개라도 비어 있을 때
                        data['Movename'] = 'c_to_t'
                        #print(data['Movename'])
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
                        
                        
                    elif(Trigger):#TODO: 물체가 있고, test machine 꽉 차 있을 때
                        data['Movename'] = 't_to_c'
                        #print(data['Movename'])
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
                        



                elif('eConv2StopperSensor' in data and data['eConv2StopperSensor'] == 0): # 물체가 없는 경우
                    number , Trigger = search_test_machine_2(tM1,tM2,tM3,tM4)  
                    if(Trigger is False): # 물체가 없고 Test machine기에 있을 때
                        data['Movename'] = 't_to_c'
                        #print(data['Movename'])
                        data['robotJoint1TargetSpeed'] = read_move(('t'+number+'_to_c'), 'motor1_speed')
                        data['robotJoint1TargetDistance'] = read_move(('t'+number+'_to_c'), 'motor1_dist')
                        data['robotJoint1Target2Distance'] = read_move(('t'+number+'_to_c'), 'motor1_dist_r')
                        data['robotJoint2TargetSpeed'] = read_move(('t'+number+'_to_c'), 'motor2_speed')
                        data['robotJoint2Target1Distance'] = read_move(('t'+number+'_to_c'), 'motor2_1_dist')
                        data['robotJoint2Target2Distance'] = read_move(('t'+number+'_to_c'), 'motor2_2_dist')
                        data['robotJoint2Target3Distance'] = read_move(('t'+number+'_to_c'), 'motor2_3_dist')
                        data['robotHandTargetSpeed'] = read_move(('t'+number+'_to_c'), 'motor3_speed')
                        data['robotHandOnTargetDistance'] = read_move(('t'+number+'_to_c'), 'motor3_handon_dist')
                        data['robotHandOffTargetDistance'] = read_move(('t'+number+'_to_c'), 'motor3_handoff_dist')
                        
                    elif(Trigger): # 모두 비어 있을 때
                        data['Movename'] = 'ini'
                        #print(data['Movename'])
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
                        
                # Total Stop Button
                if 'totalConvStopSensor' in data and data['totalConvStopSensor'] == 1:
                    data['Movename'] = 'emergency'
                    #print(data['Movename'])
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
