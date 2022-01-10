import socket
import threading
import time
import random
import sys

HOST = socket.gethostname()
PORT = 65432
print("Host: ", HOST)
print("Port: ", PORT)

amount_of_players = input("How Many Players Are Going To Play?")
try:
    amount_of_players = int(amount_of_players)
    if amount_of_players <= 1:
        sys.exit("Invalid Player Amount")
except:
    sys.exit("Invalid Player Amount")

players = []

shot = []

player_info = []
player_info_quick = []

logged = []
logG = "not"

ticks_r = False

def testrig(conn,addr):
    global ticks_r
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
                            try:
                                players.append(str(addr))

                                #player_info_quick.append(str(addr) + ":" + "x,y")
                                player_info.append(str(addr) + ":" + "100,k@x-y")
                                number = logged.__len__()
                                logged.append(number)
                                log = number
                                data = bytes("CM_" + str(log), encoding='utf-8')

                                conn.sendall(data)


                            except Exception as e:
                                pass





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
                        conn.sendto(data, addr)
                    if data == b'gk':
                        global logG
                        if not logG == "not":
                            data = bytes(str(logG), encoding='utf-8')
                            conn.sendto(data, addr)
                        else:
                            conn.sendto(b'not', addr)



        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            Break = True
            global players_count
            players_count -= 1
            try:
                logged.pop(log)
            except:
                pass
            print("Non Vital 50% of the time: ", e)

def split_player_info(info):
    a = info.split(",")
    health, more = a[0], a[1]
    a = more.split("@")
    G_K, coords = a[0], a[1]
    a = coords.split("-")
    x, y = a[0], a[1]
    return health, G_K, x, y


players_count = 0

def start_game(conn, addr):
    try:
        time.sleep(2)
        global logG
        global player_info

        try:
            logG = random.randint(0, player_info.__len__() - 1)
        except:
            print("[ERROR][MAJOR] Failed to calculate Gun / knife")
    except Exception as e:
        print("FATAL ERROR: ", e)



Started = False

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            x = threading.Thread(target=testrig, args=(conn, addr))
            x.start()
            players_count += 1
            if players_count == amount_of_players and Started == False:
                start_game(conn, addr)
                Started = True


    except:
        print("")
        print('[ERROR]: Port Already In use / Already Binded.')

        print("Is anyone else using this port / game? - Try using a different port number")
        CC = input("Press Enter To Quit: ")
        break


