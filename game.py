import pygame
import random
import time
import math

#initialize the pygame
pygame.init()

#create the screen with dimensions 800x600
screen = pygame.display.set_mode((800, 700))
clock = pygame.time.Clock()
FPS = 60

background = pygame.image.load('background.png')
#storing the dimensions of the screen
width = screen.get_width()
height = screen.get_height()

#storing colors
color_white = (255,255,255)
color_black = (0,0,0)
color_light = (175,175,175)
color_dark = (100,100,100)
color_blue = (50,50,255)

#Buttons
startbutton = pygame.image.load('startbutton.png')
startbuttonrect = startbutton.get_rect()
optionsbutton = pygame.image.load('optionsbutton.png')
optionsbuttonrect = optionsbutton.get_rect()
quitbutton = pygame.image.load('quitbutton.png')
quitbuttonrect = quitbutton.get_rect()
easybutton = pygame.image.load('easybutton.png')
easybuttonrect = easybutton.get_rect()
normalbutton = pygame.image.load('normalbutton.png')
normalbuttonrect = normalbutton.get_rect()
hardbutton = pygame.image.load('hardbutton.png')
hardbuttonrect = hardbutton.get_rect()

#fonts and texts
smallfont = pygame.font.SysFont('Corbel',35)
largefont = pygame.font.SysFont('Corbel',65)
text_quit = smallfont.render('Quit', True, color_light)
text_play = smallfont.render("Play", True, color_light)
text_options = smallfont.render("Options",True,color_light)
text_title = largefont.render("Shooter Game",True,color_blue)
titleRect = text_title.get_rect()
titleRect.center = (width/2,height*1/8)

#Title of display
pygame.display.set_caption("Shooter Game")

#Icon for display
icon = pygame.image.load('guns.png')
pygame.display.set_icon(icon)

# Player
playerIcon = pygame.image.load('player-1-1.png.png')
playerX = 400
playerY = 400
playerMoveSpeed = 5
playerXChange = 0
playerYChange = 0
playerHP = 3
score = 0

# Player Bullets (subject to change based on enemy bullet funcitonality)
bulletIcon = pygame.image.load('bullet(1).png')
bulletX = 1000
bulletY = 1000
bulletMoveSpeed = 10
bulletXChange = 0
bulletYChange = 10
global bulletState
bulletState = 'ready'

enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, dx, dy):
        super().__init__()
        self.image = pygame.image.load('Enemy-Person.png.png')
        self.x = random.randrange(200, 600)
        self.y = random.randrange(100, 200)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.xvel = random.choice([-1, 1])
        self.yvel = random.choice([-1, 1])
        self.lastfire = 0
        self.reloadspeed = 3000
    def update(self, game_time, screen):
        if self.xvel > 0:
            if self.rect.right < width:
                self.x += self.xvel
            else:
                self.xvel *= -1
        else:
            if self.rect.left > 0:
                self.x += self.xvel
            else:
                self.xvel *= -1


        if self.yvel > 0:
            if self.rect.bottom < height:
                self.y += self.yvel
            else:
                self.yvel *= -1
        else:
            if self.rect.top > 100:
                self.y += self.yvel
            else:
                self.yvel *= -1

        self.rect.center = (self.x, self.y)
        diff = game_time - self.lastfire
        if diff >= self.reloadspeed:
            self.fire(screen)
            self.lastfire = game_time

    def draw(self, screen):
        screen.blit(int(self.rect.x), int(self.rect.y), self.rect)

    def fire(self, screen):
        vel = 0
        if playerY < self.rect.y:
            vel = -4
            bullet = enemyBullet(self.rect.x, self.rect.y, vel, 'bullet(1).png')
        elif playerY > self.rect.y:
            vel = 4
            bullet = enemyBullet(self.rect.x, self.rect.y, vel, 'enemyBullet.png')
        bullet_group.add(bullet)

class enemyBullet(pygame.sprite.Sprite):
    def __init__(self, dx, dy, vel, pic):
        super().__init__()
        self.image = pygame.image.load(pic)
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        self.yvel = vel
    def update(self):
        self.rect.y += self.yvel

        if self.rect.y > height or self.rect.y < 0:
            self.kill()
    def draw(self, screen):
        screen.blit(self.image, self.rect)


enemies = [Enemy(400, 50), Enemy(600, 50), Enemy(200, 50)]
for enemy in enemies:
    enemy_group.add(enemy)

# Not yet working, for when enemy bullet hits player
# def playerHit(enemyBulletX, enemyBulletY, playerX, playerY):
#     # Decrease playerHP
#     return True

# For player bullet functionality, shoots bullets.
def fireBullet(x, y):
    global bulletState
    bulletState = 'fire'
    screen.blit(bulletIcon, (x + 4, y))

# To draw the player on screen
def player(x, y):
    screen.blit(playerIcon,(x, y))

# To calculate if this is a collision or not (True -> collision, False -> No collision)
def collision(x1, y1, x2, y2):
    if math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2)) < 20:
        return True
    else:
        return False

# To display a text when the player loses
def gameOver():
    font = pygame.font.Font('freesansbold.ttf', 64)
    gameOverText = font.render('You Died', True, (0, 0, 0))
    screen.blit(gameOverText, (250, 250))

# To display the player's current HP in the top left
def displayHP():
    font = pygame.font.Font('freesansbold.ttf', 20)
    hp = font.render('HP: ' + str(playerHP), True, (0, 0, 0))
    screen.blit(hp, (10, 10))

# To display the player's current score in the top right
def displayScore():
    font = pygame.font.Font('freesansbold.ttf', 20)
    Score = font.render('Score: ' + str(score), True, (0, 0, 0))
    screen.blit(Score, (width - 120, 10))

#game loop for window
bullet = False
running = False
in_menu = True
in_options = False

#Drawing the menu if in the menu
while in_menu:
    #make background white
    #screen.fill((255, 255, 255))
    screen.blit(background, (0, -80))

    #stores mouse position
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():

        #closing the window if red x is clicked
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        #mouse interactions -- in progress
        if event.type == pygame.MOUSEBUTTONDOWN:
             #mouse controls on the menu
             if in_menu:
                if 266.5 <= mouse[0] <= 533.5 and 500 <= mouse[1] <= 600:
                    running = False
                    in_menu = False
                    pygame.quit()
                if 266.5 <= mouse[0] <= 533.5 and 350 <= mouse[1] <= 450:
                    in_menu = False
                    in_options = True
                if 266.5 <= mouse[0] <= 533.5 and 200 <= mouse[1] <= 300:
                    in_menu = False
                    running = True

        #drawing the buttons for the menu
        #Quit button
        quitbuttonrect.center = (400, 550)
        screen.blit(quitbutton, quitbuttonrect)
        #Options button
        optionsbuttonrect.center = (400, 400)
        screen.blit(optionsbutton, optionsbuttonrect)
        #Play button
        startbuttonrect.center = (400, 250)
        screen.blit(startbutton, startbuttonrect)
        #Title text
        #screen.blit(text_title,titleRect)

        pygame.display.update()

easy_mode = False
normal_mode = True
hard_mode = False
while in_options:
    screen.blit(background, (0, -80))

    #stores mouse position
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():

        #closing the window if red x is clicked
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
                #mouse controls on the menu
                if in_options:
                    if 266.5 <= mouse[0] <= 533.5 and 200 <= mouse[1] <= 300:
                        easy_mode = True
                    if 266.5 <= mouse[0] <= 533.5 and 350 <= mouse[1] <= 450:
                        normal_mode = True
                    if 266.5 <= mouse[0] <= 533.5 and 500 <= mouse[1] <= 600:
                        hard_mode = True
                

    #Easy Button
    easybuttonrect.center = (400, 250)
    screen.blit(easybutton, easybuttonrect)
    #Normal button
    normalbuttonrect.center = (400, 400)
    screen.blit(normalbutton, normalbuttonrect)
    #Hard button
    hardbuttonrect.center = (400, 550)
    screen.blit(hardbutton, hardbuttonrect)

    pygame.display.update()



while running:
    #make background white
    time = pygame.time.get_ticks()
    clock.tick(FPS)
    # Edited so that it spawns one new enemy every 10 secs
    if time % 600 == 0:
        enemies.append(Enemy(600, 50))
        enemy_group.add(enemies[len(enemies)-1])
    enemy_group.update(time, screen)
    bullet_group.update()
    screen.blit(background, (0, -80))
    #screen.fill((255, 255, 255))

    #stores mouse position
    mouse = pygame.mouse.get_pos()
    bullet_group.draw(screen)
    enemy_group.draw(screen)
    for event in pygame.event.get():

        #closing the window if red x is clicked
        if event.type == pygame.QUIT:
            running = False
        # For Player Movement
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange += -playerMoveSpeed
            if event.key == pygame.K_RIGHT:
                playerXChange += playerMoveSpeed
            if event.key == pygame.K_UP:
                playerYChange += -playerMoveSpeed
            if event.key == pygame.K_DOWN:
                playerYChange += playerMoveSpeed
            if event.key == pygame.K_SPACE and bulletState == 'ready':
                bulletX = playerX
                bulletY = playerY
                fireBullet(bulletX, bulletY)
        elif event.type == pygame.KEYUP:
            #if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
               # playerXChange = 0
                #playerYChange = 0
            if event.key == pygame.K_LEFT:
                playerXChange -= -playerMoveSpeed
            if event.key == pygame.K_RIGHT:
                playerXChange -= playerMoveSpeed
            if event.key == pygame.K_UP:
                playerYChange -= -playerMoveSpeed
            if event.key == pygame.K_DOWN:
                playerYChange -= playerMoveSpeed


    #placeholder

    # Player Movement
    playerX += playerXChange
    playerY += playerYChange

    # BOUNDS FOR PLAYER
    if playerX <= 0:
        playerX = 0
    elif playerX >= width-32:
        playerX = 800-32

    if playerY <= 100:
        playerY = 100
    elif playerY >= height-64:
        playerY = height-64

    # BULLETS FUNCTIONALITY
    if bulletY <= 0:
        bulletY = playerY
        bulletState = 'ready'
    if bulletState == 'fire':
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange

    # For collision on enemies, removes enemy from screen after shooting it
    for i in range (len(enemies)):
        if collision(bulletX, bulletY, enemies[i].rect.x, enemies[i].rect.y + 16):
            enemy_group.remove(enemies[i])
            enemies[i] = Enemy(900, -100)
            bulletState = "ready"
            bulletX = 0
            bulletY = 0
            score += 1
    # Respawns 3 enemies if you kill all of them
    if not enemy_group:
        for i in range(3):
            enemies[i] = Enemy(random.randint(64,800-64), random.randint(64,300))
            enemy_group.add(enemies[i])


    # For collision on player
    for bullet in iter(bullet_group):
        if collision(bullet.rect.x, bullet.rect.y, playerX, playerY):
            playerHP -= 1
            bullet_group.remove(bullet)

    # To decide whether its game over or not
    if playerHP <= 0:
        gameOver()
        playerX = 900
        playerY = -100
    else:
        player(playerX, playerY)
        displayHP()
    
    #display score
    displayScore()



    pygame.display.update()
