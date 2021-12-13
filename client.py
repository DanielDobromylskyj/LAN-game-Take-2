import socket
import time
import pygame

HOST = 'DESKTOP-J5RPN01'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        time.sleep(0.5)

        # Validate Connection

        connected = False
        while True:
            if connected == True:
                # start game
                s.sendall(b'd_2,1')




























            else:
                s.sendall(b'con')
                data = s.recv(1024)
                if data == b'CM':
                    connected = True