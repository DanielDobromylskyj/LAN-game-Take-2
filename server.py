import socket
import threading
import time

HOST = socket.gethostname()
PORT = 65432
print("Host: ", HOST)
print("Port: ", PORT)

players = []

player_info = []
player_info_quick = []
logged = []
ticks_r = False

def testrig(conn,addr):
    global ticks_r
    Break = False
    if ticks_r == False:
        t = threading.Thread(target=tick, args=(conn, addr))
        t.start()
        ticks_r = True
        log = 0
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
                            try:
                                players.append(str(addr))

                                #player_info_quick.append(str(addr) + ":" + "x,y")
                                player_info.append(str(addr) + ":" + "100,k@x-y")
                                number = logged.__len__()
                                logged.append(number)
                                log = number
                                conn.sendall(b'CM')
                                print(player_info)

                            except Exception as e:
                                print(e)
                                print("[ERROR] A Major Error Has Ocured! Is this version stable? A Player has failed to join")




                    else:
                        conn.sendall(b'Failed To Connect Game Full') # not working


                else:

                    if data.startswith(b'data_'):
                        try:
                            a = data.split(b'data_') # data format (health,k or g@x-y)
                            recv = a[1]
                            recv = recv.decode("utf-8")

                            player_info.pop(log)
                            player_info.insert(log, recv)


                        except Exception as e:
                            print(e)
                            print("[ERROR] A Major Error Has Ocured! Is this version stable? Player info has failed")



                    if data == b'rd': # rd >>> read data - send back all needed player data
                        data = bytes(str(player_info), encoding='utf-8')
                        #s.sendall(data)

                        conn.sendto(data, addr)

        except Exception as e:
            print("Player Disconnected / Timed Out. Rejected Connection")
            Break = True
            global players_count
            players_count -= 1
            #print(e)



players_count = 0

def tick( conn, addr):
    pass
    #CC = input("Press Enter To Start The Game!")
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


