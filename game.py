import pygame

#initialize the pygame
pygame.init()

#create the screen with dimensions 800x600
screen = pygame.display.set_mode((800, 600))

#storing the dimensions of the screen
width = screen.get_width()
height = screen.get_height()

#storing colors
color_white = (255,255,255)
color_black = (0,0,0)
color_light = (175,175,175)
color_dark = (100,100,100)

#fonts and texts
smallfont = pygame.font.SysFont('Corbel',35)
text_quit = smallfont.render('Quit', True, color_light)
text_play = smallfont.render("Play", True, color_light)
text_options = smallfont.render("Options",True,color_light)

#Title of display
pygame.display.set_caption("Shooter Game")

#Icon for display
icon = pygame.image.load('guns.png')
pygame.display.set_icon(icon)

# Player
playerIcon = pygame.image.load('player.png')
playerX = 400
playerY = 400
playerXChange = 0
playerYChange = 0
playerHP = 5

# Player Bullets (subject to change based on enemy bullet funcitonality)
bulletIcon = pygame.image.load('bullet(1).png')
bulletX = 640
bulletY = 600
bulletXChange = 0
bulletYChange = 2
global bulletState
bulletState = 'ready'

#

#Enemy
enemyImg = pygame.image.load('player.png')
enemyX = 400
enemyY = 50
enemyX_change = 0.1

def enemy(x, y):
    #drawing the enemy image on the screen
    screen.blit(enemyImg, (x, y))

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

bulletImg = pygame.image.load('bullet.png')
enemyBulletX = 400
enemyBulletY = 50
enemyBulletY_change = 0.1

delay = 500
bullet_event = pygame.USEREVENT + 1
pygame.time.set_timer(bullet_event, delay)

def enemy_bullet(x,y):
    screen.blit(bulletImg, (x,y))


#game loop for window
bullet = False
running = True
in_menu = True
in_options = False
while running:
    #make background white
    screen.fill((255,255,255))
    #stores mouse position
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():

        #closing the window if red x is clicked
        if event.type == pygame.QUIT:
            running = False

        #mouse interactions -- in progress
        if event.type == pygame.MOUSEBUTTONDOWN:
            #mouse controls on the menu
            if in_menu:
                if width/3 <= mouse[0] <= width*2/3 and height*6/8 <= mouse[1] <= height*6/8 + 40:
                    running = False
                    pygame.quit()
                if width/3 <= mouse[0] <= width*2/3 and height*4/8 <= mouse[1] <= height*4/8 + 40:
                    in_options = True
                if width/3 <= mouse[0] <= width*2/3 and height*4/8 <= mouse[1] <= height*4/8 + 40:
                    in_menu = False
        if event.type == bullet_event:
            enemyBulletX = enemyX
            enemyBulletY += enemyBulletY_change
            bullet = True;

        # For Player Movement
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -0.5
            elif event.key == pygame.K_RIGHT:
                playerXChange = 0.5
            elif event.key == pygame.K_UP:
                playerYChange = -0.5
            elif event.key == pygame.K_DOWN:
                playerYChange = 0.5
            elif event.key == pygame.K_SPACE and bulletState is 'ready':
                bulletX = playerX
                bulletY = playerY
                fireBullet(bulletX, bulletY)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerXChange = 0
                playerYChange = 0


    #Drawing the menu if in the menu
    if in_menu:
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
            

    if enemyX <= 0:
        enemyX_change = 0.1
    elif enemyX >= 736:
        enemyX_change = -0.1

    if bullet:
        enemy_bullet(enemyBulletX, enemyBulletY)
    enemyX += enemyX_change
    enemy(enemyX, enemyY)
    
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
    if bulletState is 'fire':
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYChange

    player(playerX, playerY)

    pygame.display.update()
