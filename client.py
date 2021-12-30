import socket
import time
import pygame

HOST = 'DESKTOP-J5RPN01'  # The server's hostname or IP address DESKTOP-J5RPN01
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

                class Player():
                    def __init__(self, x, y):
                        self.images_right = []
                        self.images_left = []
                        self.index = 0
                        self.counter = 0
                        for num in range(1, 5):
                            img_right = pygame.image.load(f'img/player{num}.png')
                            img_right = pygame.transform.scale(img_right, (40, 40))
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

                    def update(self):
                        dx = 0
                        dy = 0
                        walk_cooldown = 5

                        key = pygame.key.get_pressed()
                        if key[pygame.K_UP] and self.jumped == False:
                            self.vel_y = -1
                            self.jumped = True
                        if key[pygame.K_UP] == False and self.vel_y == 0:
                            self.jumped = False
                        if key[pygame.K_LEFT]:
                            dx -= 1
                            self.counter += 1
                            self.direction = -1
                        if key[pygame.K_RIGHT]:
                            dx += 1
                            self.counter += 1
                            self.direction = 1
                        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                            self.counter = 0
                            self.index = 0
                            if self.direction == 1:
                                self.image = self.images_right[self.index]
                            if self.direction == -1:
                                self.image = self.images_left[self.index]

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
                        self.vel_y += 0.006
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
                        win.blit(self.image, self.rect)
                        pygame.draw.rect(win, (255, 255, 255), self.rect, 2)
                    # win.blit(self.FOW, (self.rect.x - 600, self.rect.y - 400))


                class World():
                    def __init__(self, data):
                        self.tile_list = []

                        # load images

                        border = pygame.image.load('img/border.png')
                        statsbar = pygame.image.load('img/SBG.png')

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

                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
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
                    world.draw()
                    player.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False

                    pygame.display.update()
                    s.sendall(b'ping')

                pygame.quit()








            else:
                print("Attempting Connection...")
                s.sendall(b'con')
                data = s.recv(1024)
                if data == b'CM':
                    connected = True
                    print("Connection Made With " + HOST + " On Port " + str(PORT))

                    screen_width = 1000
                    screen_height = 500 + 150

                    win = pygame.display.set_mode((screen_width, screen_height))
                    pygame.display.set_caption("Never Bring A Knife To A Gun Fight.")

                    # load images

                    backdrop = pygame.image.load("img/backdrop.png")
