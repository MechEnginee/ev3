import socket
import threading
import json

ip = '10.81.98.63'
port = 8001
address = (ip, port)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)

server_socket.listen(10)


data = dict()


def server_thread(client_socket, client_addr):
    print('Thread Created')
    try:
        while True:
            msg = client_socket.recv(1024).decode()

            recv_data = json.loads(msg)
            # print(recv_data)
            return_data = dict()

            for key, value in recv_data.items():
                if key == 'request':
                    for request_key in value:
                        try:
                            return_data[request_key] = data[request_key]
                        except:
                            pass
                else:
                    data[key] = value

            client_socket.send(json.dumps(return_data).encode())

            # print(json.dumps(return_data))
    except:
        client_socket.close()

threads = []

while True:
    client_socket, client_addr = server_socket.accept()
    print('connection created')
    
    
    threads.append(threading.Thread(target=server_thread, args=(client_socket, client_addr)))
    threads[-1].start()

    