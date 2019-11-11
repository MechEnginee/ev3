import os
import sys
import configparser
import struct
import redis

def get_file_name():
    return os.path.splitext(os.path.basename(sys.argv[0]))[0]

def load_config(ini_path='server_ev3.ini'):
    current_file_name = get_file_name()
    ev3_name = current_file_name.replace('server_', '')

    config = configparser.ConfigParser()
    config.read(ini_path)
    return config[ev3_name]['ip'].replace('"', ''), int(config[ev3_name]['port']), int(config[ev3_name]['size'])

def int_to_bytes(v):
    return v.to_bytes(4, 'big')

def float_to_bytes(v):
    return struct.pack('!f', v)

def bool_to_bytes(b):
    return b.to_bytes(1, 'big')

def bytes_to_int(b):
    return int.from_bytes(b, 'big')

def bytes_to_float(b):
    return struct.unpack('!f', b)[0]

def bytes_to_bool(b):
    return bool.from_bytes(b, 'big')

def connect_redis(ini_path='server_ev3.ini'):
    config = configparser.ConfigParser()
    config.read(ini_path)

    host, port = config['redis']['host'], config['redis']['port']
    return redis.Redis(host=host, port=port)

def get_conveyor_move_speed(ini_path='move.ini'):
    config = configparser.ConfigParser()
    config.read(ini_path)
    return config['conveyor']['move_speed']

if __name__ == '__main__':
    print(int_to_bytes(123))