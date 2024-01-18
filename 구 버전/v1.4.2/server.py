import socket
import time

server_ip     = "127.0.0.1"
server_port   = 3001
bufferSize  = 1024
server_addr_port = (server_ip, server_port)
client_addr_port = (server_ip, server_port)

# 데이터그램 소켓을 생성
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# 주소와 IP로 Bind
UDPServerSocket.bind((server_ip, server_port))

print("UDP server up and listening")

# 들어오는 데이터그램 Listen
while(True):
    clientMsg = ''
    client_data = ''
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    print(bytesAddressPair)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    #client_port = bytesAddressPair[2]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    #ClientPort = "Client PORT:{}".format(client_port)

    print(clientMsg)
    print(clientIP)

    if clientMsg.find('101'):
      print('program start ok')
      client_pt_num = '201'
      client_data = time.strftime('%y%m%d%H%M%S,') + client_pt_num
      bytes_to_send = str.encode(client_data)
      UDPServerSocket.sendto(bytes_to_send, (address[0], 1234))
      print('program start send')
      
