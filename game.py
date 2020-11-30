import pygame

#initialize the pygame
pygame.init()

#create the screen with dimensions 800x600
screen = pygame.display.set_mode((800, 600))

#Title of display
pygame.display.set_caption("Shooter Game")

#Icon for display
icon = pygame.image.load('guns.png')
pygame.display.set_icon(icon)

#Enemy
enemyImg = pygame.image.load('player.png')
enemyX = 400
enemyY = 50
enemyX_change = 0.1

def enemy(x, y):
    #drawing the enemy image on the screen
    screen.blit(enemyImg, (x, y))

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
while running:
    #make background white
    screen.fill((255,255,255))
    for event in pygame.event.get():
        #closing the window if red x is clicked
        if event.type == pygame.QUIT:
            running = False
        elif event.type == bullet_event:
            enemyBulletX = enemyX
            enemyBulletY += enemyBulletY_change
            bullet = True;
            

    if enemyX <= 0:
        enemyX_change = 0.1
    elif enemyX >= 736:
        enemyX_change = -0.1

    if bullet:
        enemy_bullet(enemyBulletX, enemyBulletY)
    enemyX += enemyX_change
    enemy(enemyX, enemyY)
    pygame.display.update()