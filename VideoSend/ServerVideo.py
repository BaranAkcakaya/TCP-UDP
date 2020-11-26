# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 17:21:44 2020

@author: lenovoz
"""

import pickle
import socket
import struct

import cv2

HOST = '192.168.1.63'
PORT = 8089

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

data = b'' ### CHANGED
payload_size = struct.calcsize("L") ### CHANGED

while True:

    # Retrieve message size
    
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Extract frame
    frame = pickle.loads(frame_data)
    # print(frame)
    
    dataS = pickle.dumps(frame)

    # Send message length first
    message_size = struct.pack("L", len(dataS)) ### CHANGED
    # Then data
    conn.sendall(message_size + dataS)
    

cv2.destroyAllWindows() 
s.close()