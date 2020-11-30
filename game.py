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
    pygame.display.update()