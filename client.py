import socket
import cv2
import pickle 
import struct

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.43.102' 
port = 9999
print("Socket Created Successfully\n")

client_socket.connect((host_ip,port))
data = b""
payload_size = struct.calcsize("Q")
print("Connection Builded...!!\n")


while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) # 4K
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("client video",frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break
cv2.destroyAllWindows()
client_socket.close()

