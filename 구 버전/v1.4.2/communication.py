import socket
import threading
import time
import re
 
# 클라이언트가 보내고자 하는 서버의 IP와 PORT
server_ip = "127.0.0.1"
buffersize = 1024
 
# 소켓을 UDP로 열고 서버의 IP/PORT를 연결한다. 그리고 Non-blocking로 바꾼다.

# udp_server_socket.settimeout(1.0)
 
print("UDP server is up and listening")
#udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#udp_server_socket.bind(server_addr_port)
udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_server_socket.bind((server_ip, 1234))
def received():
    byte_addr_pair = udp_server_socket.recvfrom(buffersize)
    msg  = byte_addr_pair[0]
    addr = byte_addr_pair[1]

    print(msg)
    print(addr)
    
    client_pt_num = ''
    result_msg = ''
    lastrest = []
    result_msg = ''
    msg = msg.decode('utf-8')
    if msg.find('201'):
        print('program start ok')
        client_pt_num = '301'

    elif msg.find('202'):
        print('status receive ok')
        client_pt_num = '302'
        
    elif msg.find('203'):
        print('gps receive ok')
        client_pt_num = '303'

    elif msg.find('204'):
        print('joycon receive ok')
        client_pt_num = '304'
    
    if client_pt_num != '':    
        client_data = time.strftime('%y%m%d%H%M%S,') + client_pt_num
        bytes_to_send = str.encode(client_data)
        udp_server_socket.sendto(bytes_to_send, (addr[0], addr[1]))

    for msg in re.finditer(',', msg):
        print(msg.start())
        lastrest.append(msg.start)
        
    if len(lastrest) > 1:
        #global result_msg
        result_msg = msg[int(lastrest[1])+1:]
        #return result_msg


def start_send():
    server_ip     = "127.0.0.1"
    server_port = 3001
    server_addr_port = (server_ip, server_port)
    client_pt_num = '101'
    client_data = time.strftime('%y%m%d%H%M%S,') + client_pt_num
    bytes_to_send = str.encode(client_data)
    udp_server_socket2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket2.sendto(bytes_to_send, server_addr_port)
    print('start_send()')

def status_request():
    server_ip     = "127.0.0.1"
    server_port = 3001
    server_addr_port = (server_ip, server_port)
    client_pt_num = '102'
    client_data = time.strftime('%y%m%d%H%M%S,') + client_pt_num
    bytes_to_send = str.encode(client_data)
    udp_server_socket2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket2.sendto(bytes_to_send, server_addr_port)

def status_request(gpslist):
    client_pt_num = '103'
    server_ip     = "127.0.0.1"
    server_port = 3001
    server_addr_port = (server_ip, server_port)
    client_data = time.strftime('%y%m%d%H%M%S,') + client_pt_num + str(gpslist)
    bytes_to_send = str.encode(client_data)
    udp_server_socket2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket2.sendto(bytes_to_send, server_addr_port)

def joycon_send(x, y):
    client_pt_num = '104' #조이콘 x, y 좌표 전송
    server_ip     = "127.0.0.1"
    server_port = 3001
    server_addr_port = (server_ip, server_port)
    client_data = time.strftime('%y%m%d%H%M%S,') + client_pt_num + str(x) +(',') + str(y)
    bytes_to_send = str.encode(client_data)
    udp_server_socket2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket2.sendto(bytes_to_send, server_addr_port)


  
 
#t = threading.Thread(target=received, args=(1, 100000))
#t.start()
