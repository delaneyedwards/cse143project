import pygame
import random
import time
import math

#initialize the pygame
pygame.init()

#create the screen with dimensions 800x600
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock

#storing the dimensions of the screen
width = screen.get_width()
height = screen.get_height()

#storing colors
color_white = (255,255,255)
color_black = (0,0,0)
color_light = (175,175,175)
color_dark = (100,100,100)
color_blue = (50,50,255)

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
playerXChange = 0
playerYChange = 0
playerHP = 5

# Player Bullets (subject to change based on enemy bullet funcitonality)
bulletIcon = pygame.image.load('bullet(1).png')
bulletX = 1000
bulletY = 1000
bulletXChange = 0
bulletYChange = 2
global bulletState
bulletState = 'ready'

enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, dx, dy):
        super().__init__()
        self.image = pygame.image.load('player.png')
        self.x = random.randrange(200, 600)
        self.y = random.randrange(50, 100)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.xvel = random.choice([-0.25, 0.25])
        self.yvel = random.choice([-0.25, 0.25])
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
            if self.rect.top < height:
                self.y += self.yvel
            else:
                self.yvel *= -1
        else:
            if self.rect.bottom > 0:
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
            vel = -1
            bullet = enemyBullet(self.rect.x, self.rect.y, vel, 'bullet(1).png')
        elif playerY > self.rect.y:
            vel = 1
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

#game loop for window
bullet = False
running = False
in_menu = True
in_options = False

#Drawing the menu if in the menu
while in_menu:
    #make background white
    screen.fill((255,255,255))
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
                if width/3 <= mouse[0] <= width*2/3 and height*6/8 <= mouse[1] <= height*6/8 + 40:
                    running = False
                    in_menu = False
                    pygame.quit()
                if width/3 <= mouse[0] <= width*2/3 and height*4/8 <= mouse[1] <= height*4/8 + 40:
                    in_options = True
                if width/3 <= mouse[0] <= width*2/3 and height*4/8 <= mouse[1] <= height*4/8 + 40:
                    in_menu = False
                    running = True

        #drawing the buttons for the menu
        #Quit button
        pygame.draw.rect(screen,color_dark,[width/3,height*6/8,width/3,40])
        screen.blit(text_quit,(width/2,height * 6/8))
        #Options button
        pygame.draw.rect(screen,color_dark,[width/3,height*5/8,width/3,40])
        screen.blit(text_options,(width/2,height * 5/8))
        #Play button
        pygame.draw.rect(screen,color_dark,[width/3,height*4/8,width/3,40])
        screen.blit(text_play,(width/2,height * 4/8))
        #Title text
        screen.blit(text_title,titleRect)

        pygame.display.update()

while running:
    #make background white
    time = pygame.time.get_ticks()
    # Edited so that it spawns one new enemy every 10 secs
    if time % 10000 == 0:
        enemies.append(Enemy(600, 50))
        enemy_group.add(enemies[len(enemies)-1])
    enemy_group.update(time, screen)
    bullet_group.update()
    screen.fill((255,255,255))
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
                playerXChange += -0.5
            if event.key == pygame.K_RIGHT:
                playerXChange += 0.5
            if event.key == pygame.K_UP:
                playerYChange += -0.5
            if event.key == pygame.K_DOWN:
                playerYChange += 0.5
            if event.key == pygame.K_SPACE and bulletState == 'ready':
                bulletX = playerX
                bulletY = playerY
                fireBullet(bulletX, bulletY)
        elif event.type == pygame.KEYUP:
            #if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
               # playerXChange = 0
                #playerYChange = 0
            if event.key == pygame.K_LEFT:
                playerXChange -= -0.5
            if event.key == pygame.K_RIGHT:
                playerXChange -= 0.5
            if event.key == pygame.K_UP:
                playerYChange -= -0.5
            if event.key == pygame.K_DOWN:
                playerYChange -= 0.5


    #placeholder
    
    # Player Movement
    playerX += playerXChange
    playerY += playerYChange

    # BOUNDS FOR PLAYER
    if playerX <= 0:
        playerX = 0
    elif playerX >= 800-64:
        playerX = 800-64
    
    if playerY <= 0:
        playerY = 0
    elif playerY >= 600-64:
        playerY = 600-64

    # BULLETS FUNCTIONALITY
    if bulletY <= 0:
        bulletY = playerY
        bulletState = 'ready'
    if bulletState == 'fire':
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange

    # For collision on enemies, removes enemy from screen after shooting it
    for i in range (len(enemies)):
        if collision(bulletX, bulletY, enemies[i].rect.x + 16, enemies[i].rect.y + 16):
            enemy_group.remove(enemies[i])
            enemies[i].kill()
            bulletState = "ready"
            bulletX = 0
            bulletY = 0
    # Respawns 3 enemies if you kill all of them
    if not enemy_group:
        for i in range(3):
            enemies[i] = Enemy(random.randint(64,800-64), random.randint(64,300))
            enemy_group.add(enemies[i])
    # if collision(bulletX, bulletY, playerX, playerY):
    #     playerHP -= 1
    
    # Temporary until we get a game over screen
    if playerHP == 0:
        print("game over")
        playerHP -= 1

    player(playerX, playerY)

    pygame.display.update()
