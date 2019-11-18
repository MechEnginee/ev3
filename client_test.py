import socket
import json
import random
import time

send_data_names = input('names of send data:').split(',')
recieve_data_names = input('names of recieve_data').split(',')
print(send_data_names, recieve_data_names)


# Socket Setting
ip = '192.168.10.161'
port = 8080
address = (ip, port)

# Connecting
client_socekt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socekt.connect(address)


while True:
    send_data = dict()
    for send_data_name in send_data_names:
        send_data[send_data_name] = random.randint(1, 10)
    send_data['request'] = recieve_data_names
    print(json.dumps(send_data))

    client_socekt.send(json.dumps(send_data).encode())

    recieve_msg = client_socekt.recv(1024).decode()
    recieve_data = json.loads(recieve_msg)
    print(recieve_data)
    
    time.sleep(random.random())
