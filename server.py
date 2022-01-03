import socket
import threading
import time

HOST = socket.gethostname()
PORT = 65432
print("Host: ", HOST)
print("Port: ", PORT)

players = []

ticks_r = False

def testrig(conn,addr):
    global ticks_r
    Break = False
    if ticks_r == False:
        t = threading.Thread(target=tick, args=(conn, addr))
        t.start()
        ticks_r = True
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
            global players_count
            players_count -= 1



players_count = 0

def tick( conn, addr):
    CC = input("Press Enter To Start The Game!")
    #with conn:
    #    while True:
    #        conn.sendall(b'tick')
    #        time.sleep(0.01)


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


