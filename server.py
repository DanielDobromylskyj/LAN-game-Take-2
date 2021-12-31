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
    Break = False
    with conn:
        try:
            while True:
                if Break == True:
                    break
                data = conn.recv(1024)
                if not data:
                    break
                if data == b'ping':
                    conn.sendall(b'pong')
                elif data == b'con':
                    if not players.__len__() > 4:
                        if players.count(addr) == 1:
                            conn.sendall(b'Failed To Connect Game Full')  # not working
                        else:
                            players.append(addr)

                            conn.sendall(b'CM')
                            print("player connected")



                    else:
                        conn.sendall(b'Failed To Connect Game Full') # not working


                else:
                    if data.startswith(b'd'):
                        #player_data =  "<" + (data.split(b"_")) + "..." + addr + ">"
                        pass


                    if data == b'rd': # rd >>> read data - send back all needed player data
                        print("DATA REQUEST")
        except:
            print("Player Disconnected / Timed Out. Rejected Connection")
            Break = True

players_count = 0

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            x = threading.Thread(target=testrig, args=(conn, addr))
            x.start()
            players_count += 1
    except:
        print("")
        print("")
        print("")
        print('[ERROR]: Port Already In use / Already Binded.')

        print("Is anyone else using this port / game? - Try using a different port number")
        CC = input("Press Enter To Quit: ")
        break


