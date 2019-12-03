import os
import sys
import socket
import time
import configparser
import json
import struct
import datetime



# ev3 Name
ev3_name = 'MCD_IoT'
# -----------------------------------------------------------------------

# Socket Setting
ip='10.81.34.137'
port=8001
address = (ip, port)

# Connecting
ev3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ev3_socket.connect(address)
ev3_socket.send(ev3_name.encode('utf-8'))


while True:

    # Receive data
    try:
        recieve_msg = ev3_socket.recv(1024).decode('utf-8')
        recieve_data = json.loads(recieve_msg)
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print ('Decoding JSON has failed')
    print(recieve_data)
    time.sleep(1)