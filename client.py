import socket
import sys
import time
import pygame
import ast
import os
import threading

HOST = input("Server Ip / Name: ")  # The server's hostname or IP address DESKTOP-J5RPN01
PORT = input("Port from Server: ")    # The port used by the server
if HOST == ".":
    HOST = 'DESKTOP-J5RPN01'
    PORT = 65432

global character
G_K = "UNKNOWN"

adresses = ""

bullets = []
bullet_png = pygame.image.load("img/bullet.png")

gun_display = pygame.image.load("img/gun_display.png")
knife_display = pygame.image.load("img/knife_display.png")

try:
    PORT = int(PORT)
except:
    print("Port may have failed. Still Continuing.")

reconnects = 0

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            time.sleep(0.5)


            # Validate Connection

            connected = False
            while True:
                if connected == True:
                    # start game

                    def shoot(x, y ,direction):
                        global bullets

                        Hit = False
                        dx = x
                        dy = y + 30

                        while Hit == False:
                            if direction == 1:
                                dx += 10
                            elif direction == -1:
                                dx -= 10
                            else:
                                pass

                            if dx == x:
                                print("Bad Bullet | Not Shot")
                                break
                            else:
                                time.sleep(0.0001)

                            for tile in world.tile_list:
                                # check for collision on wall
                                if tile[1].collidepoint(dx, dy):
                                    Hit = True

                            # check for player colition needed

                            win.blit(bullet_png, (dx, dy))

                    class Player():
                        def __init__(self, x, y):
                            self.images_right = []
                            self.images_left = []
                            self.index = 0
                            self.counter = 0
                            for num in range(1, 5):
                                img_right = pygame.image.load(f'img/player{num}.png')
                                img_right = pygame.transform.scale(img_right, (30, 60))
                                img_left = pygame.transform.flip(img_right, True, False)
                                self.images_right.append(img_right)
                                self.images_left.append(img_left)
                            self.image = self.images_right[self.index]
                            self.rect = self.image.get_rect()
                            self.rect.x = float(x)
                            self.rect.y = float(y)
                            self.width = self.image.get_width()
                            self.height = self.image.get_height()
                            self.vel_y = 0
                            self.jumped = False
                            self.direction = 0
                            self.let_go = True

                            self.health_bar_full = pygame.image.load("img/health.png")
                            self.health_bar_cover = pygame.image.load("img/Health_Cover.png")
                            self.health_bar_border = pygame.image.load("img/Health_Border.png")


                            self.health = 100
                            self.type = "UNKNOWN"

                        def update(self):
                            dx = 0
                            dy = 0
                            walk_cooldown = 5

                            key = pygame.key.get_pressed()
                            if key[pygame.K_w] and self.jumped == False:
                                self.vel_y = -5
                                self.jumped = True
                            if key[pygame.K_w] == False and self.vel_y == 0:
                                self.jumped = False
                            if key[pygame.K_a]:
                                dx -= 3
                                self.counter += 1
                                self.direction = -1
                            if key[pygame.K_d]:
                                dx += 3
                                self.counter += 1
                                self.direction = 1
                            if key[pygame.K_d] == False and key[pygame.K_RIGHT] == False:
                                self.counter = 0
                                self.index = 0
                                if self.direction == 1:
                                    self.image = self.images_right[self.index]
                                if self.direction == -1:
                                    self.image = self.images_left[self.index]

                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if G_K == "gun":
                                        mouse_presses = pygame.mouse.get_pressed()
                                        if mouse_presses[0]:
                                            x = threading.Thread(target=shoot, args=(self.rect.x, self.rect.y, self.direction))
                                            x.start()




                            # do animation
                            if self.counter > walk_cooldown:
                                self.counter = 0
                                self.index += 1
                                if self.index >= len(self.images_right):
                                    self.index = 0
                                if self.direction == 1:
                                    self.image = self.images_right[self.index]
                                if self.direction == -1:
                                    self.image = self.images_left[self.index]

                            # gravity
                            self.vel_y += 0.1
                            if self.vel_y > 8:
                                self.vel_y = 8
                            dy += self.vel_y

                            # check for collision
                            for tile in world.tile_list:
                                # check for collision in x direction
                                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                                    dx = 0
                                # check for collision in y direction
                                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                    # check if below the ground i.e. jumping
                                    if self.vel_y < 0:
                                        dy = tile[1].bottom - self.rect.top
                                        self.vel_y = 0
                                    # check if above the ground i.e. falling
                                    elif self.vel_y >= 0:
                                        dy = tile[1].top - self.rect.bottom
                                        self.vel_y = 0

                            # update player coordinates

                            self.rect.x += dx
                            self.rect.y += dy

                            if self.rect.bottom > screen_height:
                                self.rect.bottom = screen_height
                                dy = 0

                            # draw player onto screen
                            #win.blit(self.image, self.rect)
                            #pygame.draw.rect(win, (255, 255, 255), self.rect, 2)
                            #win.blit(self.FOW, (self.rect.x - 600, self.rect.y - 400))
                            strDATA = "data_" + str(self.health) + "," + G_K + "@" + str(self.rect.x) + "-" + str(self.rect.y)
                            data = bytes(strDATA, encoding='utf-8')
                            try:
                                s.sendall(data)
                            except:
                                print("DATA failed to send")
                            global character
                            character = self.image
                            win.blit(self.health_bar_full, (50, 550))
                            win.blit(self.health_bar_cover, ((-150 + (200 - (self.health * 2))), 550))
                            win.blit(self.health_bar_border, (49, 549))



                    class World():
                        def __init__(self, data):
                            self.tile_list = []

                            # load images

                            border = pygame.image.load('img/border.png')
                            statsbar = pygame.image.load('img/SBG.png')

                            plat_left = pygame.image.load('img/platform_left.png')
                            plat_right = pygame.image.load('img/platform_right.png')
                            plat_middle = pygame.image.load('img/platform.png')

                            row_count = 0
                            for row in data:
                                col_count = 0
                                for tile in row:

                                    if tile == 0:
                                        pass


                                    elif tile == 1:
                                        img = pygame.transform.scale(border, (50, 50))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * 50
                                        img_rect.y = row_count * 50
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)

                                    elif tile == 7:
                                        img = pygame.transform.scale(plat_left, (50, 50))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * 50
                                        img_rect.y = row_count * 50
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)

                                    elif tile == 8:
                                        img = pygame.transform.scale(plat_middle, (50, 50))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * 50
                                        img_rect.y = row_count * 50
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)

                                    elif tile == 9:
                                        img = pygame.transform.scale(plat_right, (50, 50))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * 50
                                        img_rect.y = row_count * 50
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)

                                    elif tile == -9:
                                        img = pygame.transform.scale(statsbar, (50, 50))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * 50
                                        img_rect.y = row_count * 50
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)

                                    col_count += 1
                                row_count += 1

                        def draw(self):
                            for tile in self.tile_list:
                                win.blit(tile[0], tile[1])


                    # World Data / Level
                    world_data = [

                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 7, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 8, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 0, 7, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [-9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9],
                        [-9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9],
                        [-9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9],

                    ]

                    player = Player(300, screen_height - 230)
                    world = World(world_data)

                    run = True



                    while run:

                        win.blit(backdrop, (0, 0))

                        wd = threading.Thread(target=world.draw)
                        wd.start()

                        pu = threading.Thread(target=player.update())
                        pu.start()

                        s.sendall(b'rd')
                        data = s.recv(1024)
                        x = data.decode("utf-8")
                        data = ast.literal_eval(x)


                        try:
                            s.sendall(b'gk')
                            data2 = s.recv(1024)
                            data2 = data2.decode("utf-8")
                            try:
                                if int(data2) == int(Log):
                                    G_K = "gun"
                                    win.blit(gun_display,(300, 550))
                                else:
                                    G_K = "knife"
                                    win.blit(knife_display, (300, 550))



                            except:
                                pass



                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            print(exc_type, exc_tb.tb_lineno)


                        for players in data:
                            coords_raw = players.split("@")
                            coords_raw = coords_raw[1].split("-")
                            x, y = coords_raw[0], coords_raw[1]

                            try:
                                win.blit(character, (int(x), int(y)))
                            except Exception as e:
                                pass

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False


                        pygame.display.flip()

                    pygame.quit()
                    break




                else:
                    try: # Connect and presses errors / get needed data
                        print("Attempting Connection...")
                        s.sendall(b'con')
                    except Exception as error1:
                        print("Connection Failed: ", error1)
                    data = s.recv(1024)
                    if data.startswith(b'CM_'):
                        CC, Binary_Log = data.split(b'_')
                        Log = Binary_Log.decode("utf-8")
                        connected = True
                        print("Connection Made With " + HOST + " On Port " + str(PORT) + " Log Number: " + Log)

                        screen_width = 1000
                        screen_height = 500 + 150

                        win = pygame.display.set_mode((screen_width, screen_height))
                        pygame.display.set_caption("Never Bring A Knife To A Gun Fight.")

                        # load images

                        backdrop = pygame.image.load("img/backdrop.png")
    except Exception as e:
        print(e)
        reconnects += 1
        if reconnects > 4:
            print("Connection Lost. Aborting.")
            time.sleep(1)
            sys.exit("Timed Out. Failed to connect 5 times. Is the server online?")
        else:
            print("Connection Lost. Reconnecting...")