# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 17:21:42 2020

@author: lenovoz
"""

import cv2
import numpy as np
import socket
import sys
import pickle
import struct

cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.63',8089))

dataS = b'' ### CHANGED
payload_size = struct.calcsize("L") ### CHANGED

while True:
    _, frame = cap.read()
    # Serialize frame
    data = pickle.dumps(frame)

    # Send message length first
    message_size = struct.pack("L", len(data)) ### CHANGED

    # Then data
    clientsocket.sendall(message_size + data)
    
    # """""""""""""""""""""""""""""""""""""""""""""
    print(len(dataS) < payload_size)
    while len(dataS) < payload_size:
        dataS += clientsocket.recv(4096)

    packed_msg_size = dataS[:payload_size]
    dataS = dataS[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

    # Retrieve all data based on message size
    while len(dataS) < msg_size:
        dataS += clientsocket.recv(4096)

    frame_data = dataS[:msg_size]
    dataS = dataS[msg_size:]

    # Extract frame
    frameS = pickle.loads(frame_data)
    print(frameS)
    
    cv2.imshow('frame', frameS)
    cv2.waitKey(1)

clientsocket.close()
cv2.destroyAllWindows() 