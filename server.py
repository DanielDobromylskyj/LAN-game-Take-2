import socket
import threading

HOST = socket.gethostname()
PORT = 65432
print("Host: ", HOST)
print("Port: ", PORT)

players = []

#x = threading.Thread(target=NewPlayer, args=(addr,))
#x.start()

def testrig(conn,addr):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            if data == b'ping':
                conn.sendall(b'pong')
            elif data == b'con':
                if not players.__len__() > 4:
                    if players.count(addr) == 1:
                        conn.sendall(b'Failed To Connect Game Full')  # not working
                        print("full")





                    else:
                        players.append(addr)

                        conn.sendall(b'CM')
                        print(addr)
                        print(players)

                else:
                    conn.sendall(b'Failed To Connect Game Full') # not working
                    print("full")


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        x = threading.Thread(target=testrig, args=(conn, addr))
        x.start()


