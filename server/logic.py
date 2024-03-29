import json
import configparser
import time
import sqlite3
import threading

switch1 = False
Flag1 = False
switch2 = False
Flag2 = False
switch3 = False
Flag3 = False
switch4 = False
Flag4 = False

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
        if(value==1):
            Trigger = False
            number = str(i+1)
            break

    return number, Trigger

def timer(tM1, tM2, tM3, tM4):
    global switch1
    global Flag1
    global switch2
    global Flag2
    global switch3
    global Flag3
    global switch4
    global Flag4
    tM1_t = 0
    tM2_t = 0
    tM3_t = 0
    tM4_t = 0
    if tM1 == 1:
        if switch1 == False:
            threading.Thread(target=test1_timer).start()
            switch1 = True
        else:
            if Flag1 == True:
                tM1_t = 1
            else:
                tM1_t = 0
    else:
        tM1_t = 0
        switch1 = False
        Flag1 = False
    
    if tM2 == 1:
        if switch2 == False:
            threading.Thread(target=test2_timer).start()
            switch2 = True
        else:
            if Flag2 == True:
                tM2_t = 1
            else:
                tM2_t = 0
    else:
        tM2_t = 0
        switch2 = False
        Flag2 = False
    
    if tM3 == 1:
        if switch3 == False:
            threading.Thread(target=test3_timer).start()
            switch3 = True
        else:
            if Flag3 == True:
                tM3_t = 1
            else:
                tM3_t = 0
    else:
        tM3_t = 0
        switch3 = False
        Flag3 = False
    
    if tM4 == 1:
        if switch4 == False:
            threading.Thread(target=test4_timer).start()
            switch4 = True
        else:
            if Flag4 == True:
                tM4_t = 1
            else:
                tM4_t = 0
    else:
        tM4_t = 0
        switch4 = False
        Flag4 = False
    return tM1_t, tM2_t, tM3_t, tM4_t

def test1_timer():
    global Flag1
    global switch1
    time.sleep(10)
    Flag1 = True

def test2_timer():
    global Flag2
    global switch2
    time.sleep(10)
    Flag2 = True

def test3_timer():
    global Flag3
    global switch3
    time.sleep(10)
    Flag3 = True

def test4_timer():
    global Flag4
    global switch4
    time.sleep(10)
    Flag4 = True

def dict_in_list(lists):
    datalist = list()
    datadict = dict()
    keys = ['Start_Flag', 'eConv1EntrySensor', 'eConv2EntrySensor', 'eConv2StopperSensor', 'tM1Sensor', 'tM2Sensor', 'tM3Sensor', 'tM4Sensor', 'rConv1EntrySensor', 'rConv2EntrySensor', 'rConv2StopperSensor' ,'eConv1Speed', 'eConv2Speed', 'eConv2StopperSpeed', 'robotJoint1Speed', 'robotJoint2Speed', 'robotHandSpeed', 'rConv1Speed', 'rConv2Speed', 'rConv2StopperSpeed', 'rConv2PushSpeed']
    queryData = lists
    for data in queryData:
        for i in range(data):
            datadict[keys[i]] = data[i]
        datalist.append(datadict)
    return datalist

def remove_start_column(lists):
    queryData = lists
    for data in queryData:
        for key, value in data.items():
            if key == 'Start_Flag':
                del data[key]
    return queryData

def log_thread(data):

    # SQL 쿼리 실행
    # cursor.execute("CREATE TABLE EV3_Sensor(eConv1EntrySensor int, eConv2EntrySensor float, eConv2StopperSensor int, tM1Sensor int, tM2Sensor int, tM3Sensor int, tM4Sensor int,rConv1EntrySensor float,rConv2EntrySensor float,rConv2StopperSensor int)")
    # conn.commit()
    # cursor.execute("CREATE TABLE EV3_Motor(eConv1Speed float, eConv2Speed float, eConv2StopperSpeed float, robotJoint1Speed float, robotJoint2Speed float, robotHandSpeed float, rConv1Speed float,rConv2Speed float,rConv2StopperSpeed float,rConv2PushSpeed float)")
    # conn.commit()
    while True:
        try:
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
            robotJoint1Position = data['robotJoint1Position'] if 'robotJoint1Position' in data else None
            robotJoint2Position = data['robotJoint2Position'] if 'robotJoint2Position' in data else None
            robotHandPosition = data['robotHandPosition'] if 'robotHandPosition' in data else None
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
            #Start_Flag
            Start_Flag = 'Start' if (eConv1EntrySensor and eConv2EntrySensor and tM1Sensor and tM2Sensor and eConv1Speed and eConv2Speed and eConv2StopperSpeed and robotJoint1Speed and robotJoint2Speed and robotHandSpeed and eConv2StopperSensor and tM3Sensor and tM4Sensor and rConv1EntrySensor and rConv2EntrySensor and rConv1Speed and rConv2Speed and rConv2StopperSpeed and rConv2PushSpeed and rConv2StopperSensor and totalConvStopSensor) != None else None

            # Insert
            cursor.execute("INSERT INTO EV3DEV VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(Start_Flag, eConv1EntrySensor, eConv2EntrySensor, eConv2StopperSensor, tM1Sensor, tM2Sensor, tM3Sensor, tM4Sensor,rConv1EntrySensor,rConv2EntrySensor,rConv2StopperSensor,eConv1Speed, eConv2Speed, eConv2StopperSpeed, robotJoint1Speed, robotJoint2Speed, robotHandSpeed, rConv1Speed, rConv2Speed, rConv2StopperSpeed, rConv2PushSpeed,robotJoint1Position,robotJoint2Position,robotHandPosition))
            conn.commit()
            
            conn.close()
            time.sleep(0.1)
        except:
            pass
    


    
    
    


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
                if data['eConv2StopperSensor'] == 1:
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
            tM1 = int(data['tM1Sensor'])
            tM2 = int(data['tM2Sensor'])
            tM3 = int(data['tM3Sensor'])
            tM4 = int(data['tM4Sensor'])
            tM1_t, tM2_t, tM3_t, tM4_t = timer(tM1, tM2, tM3, tM4)
            if len(recieved_data['request']) == 1:
                # 4. Make Return Data
                return_data = make_return_data(data, recieved_data['request'])
                # 5. Send
                client_socket.send(json.dumps(return_data).encode('utf-8'))
                
            else:

                if('eConv2StopperSensor' in data and data['eConv2StopperSensor'] == 1):
                    number , Trigger = search_test_machine_1(tM1,tM2,tM3,tM4)
                    if (Trigger is False): #물체가 있고, test machine 중에 1개라도 비어 있을 때
                        data['Movename'] = 'c_to_t'
                        data['robotJoint1TargetSpeed'] = read_move(('c_to_t'+number), 'motor1_speed')
                        data['robotJoint1TargetDistance'] = read_move(('c_to_t'+number), 'motor1_dist')
                        data['robotJoint2TargetSpeed'] = read_move(('c_to_t'+number), 'motor2_speed')
                        data['robotJoint2Target1Distance'] = read_move(('c_to_t'+number), 'motor2_1_dist')
                        data['robotJoint2Target2Distance'] = read_move(('c_to_t'+number), 'motor2_2_dist')
                        data['robotJoint2Target3Distance'] = read_move(('c_to_t'+number), 'motor2_3_dist')
                        data['robotHandTargetSpeed'] = read_move(('c_to_t'+number), 'motor3_speed')
                        data['robotHandOnTargetDistance'] = read_move(('c_to_t'+number), 'motor3_handon_dist')
                        data['robotHandOffTargetDistance'] = read_move(('c_to_t'+number), 'motor3_handoff_dist')
                        data['robotJoint1Target2Distance'] = 0 # 필요 없는 값 / None이면 에러 발생이기 때문에 추가
                        
                        
                    elif(Trigger):#TODO: 물체가 있고, test machine 꽉 차 있을 때
                        data['Movename'] = 't_to_c'
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

                    number , Trigger = search_test_machine_2(tM1_t,tM2_t,tM3_t,tM4_t)  
                    if(Trigger is False): # 물체가 없고 Test machine기에 있을 때
                        data['Movename'] = 't_to_c'
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
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                recieved_data = json.loads(msg)
                save_data(data, recieved_data)
            except:
                pass
            # 2. Save Data
            
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
            
            if 'rConv2StopperSensor' in data and (data['rConv2StopperSensor'] == 1):
                data['rConv2StopperTargetSpeed'] = read_move('stopper2', 'on_speed')
                data['rConv2StopperTargetDistance'] = read_move('stopper2', 'on_dist')
                data['rConv2PushTargetSpeed'] = read_move('push', 'on_speed')
                data['rConv2PushTargetDistance'] = read_move('push', 'on_dist')
            else :
                data['rConv2StopperTargetSpeed'] = read_move('stopper2', 'off_speed')
                data['rConv2StopperTargetDistance'] = read_move('stopper2', 'off_dist')
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
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                recieved_data = json.loads(msg)
                save_data(data, recieved_data)
            except:
                pass
            # 2. Save Data
            
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


def Simulation_data_send(client_socket, client_addr, data):#TODO:
    send_data = list()
    # try:
    # while True:
    #log db read
    # Sqlite DB Connection
    conn = sqlite3.connect("C:/Users/TJ/ev3/server/ev3dev.db")
    # Connection 으로부터 Cursor 생성
    cursor = conn.cursor()
    # DB Table column key value setting
    cursor.execute("SELECT * FROM EV3DEV WHERE Start_Flag = 'Start'")
    
    rows = cursor.fetchall()
    rowlist = dict_in_list(rows) #({key:value},{key:value},{key:value},...)
    send_data = remove_start_column(rowlist)

    #send data
    for i in range(send_data):
        client_socket.send(json.dumps(send_data[i]).encode('utf-8'))
        time.sleep(0.1)

    client_socket.close()

def MCD_IoT(client_socket, client_addr, data):
    keys = ['eConv1EntrySensor', 'eConv2EntrySensor', 'eConv2StopperSensor', 'tM1Sensor', 'tM2Sensor', 'tM3Sensor', 'tM4Sensor', 'rConv1EntrySensor', 'rConv2EntrySensor', 'rConv2StopperSensor' ,'eConv1Speed', 'eConv2Speed', 'eConv2StopperSpeed', 'robotJoint1Speed', 'robotJoint2Speed', 'robotHandSpeed', 'rConv1Speed', 'rConv2Speed', 'rConv2StopperSpeed', 'rConv2PushSpeed','robotJoint1Position','robotJoint2Position','robotHandPosition']
    return_data = {}
    try:
        while True:
            for i in keys:
                return_data[i] = data[i]
               
            try:
                # msg = client_socket.recv(1024).decode('utf-8')
                # recieved_data = json.loads(msg)
                # if msg == 'A':
                client_socket.send(json.dumps(return_data).encode('utf-8'))
                # else:
                #     pass
            except:
                pass
            # 5. Send
            # client_socket.send(json.dumps(return_data).encode('utf-8'))
            
            
    except:
        client_socket.close()