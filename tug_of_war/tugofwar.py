import pygame
import time
import math

pygame.init()

# Colors
green = (40, 158, 40)
red = (255, 0, 0)
brown = (165, 42, 42)
white = (255, 255, 255)

# Fonts
text_font = pygame.font.SysFont("Times New Roman", 80)
player_font = pygame.font.SysFont("Times New Roman", 30)

# Set up the display
back_g = pygame.display.set_mode((750, 500))
pygame.display.set_caption("Tug of War")

# Game Variables
game_exit = False
game_over = False
fps = 50
clock = pygame.time.Clock()
active_frame = 1
active_frame2 = 1
xspeed = 10
mode = 0  # 0-idle  1-right  2-left
mode1 = 0
counter = 0

# Character and Background Images
back_img = pygame.image.load("grass.png").convert()
tug_of_war=pygame.image.load("tug of war title.jpg").convert_alpha()
char1_frame = ["grey fleft.png", "grey fleft mid.png", "grey fleft last.png"]
char2_frame = ["yellow fr.png", "yellow fright mid.png", "yellow fright last.png"]

# Position of two players
px1 = 525
py1 = 250
px2 = 175
py2 = 250

# Position of rope
rx = 175
ry = 280
rex = 525
rey = 280

# Animation Function
def update_1(mode, counter):
    active_frame = 0
    if counter >= 60:
        counter = 0
    if mode == 0:
        if counter < 30:
            active_frame = 0
        if 30 <= counter < 60:
            active_frame = 0
    if mode == 1:
        if counter < 30:
            active_frame = 1
        if 30 <= counter < 60:
            active_frame = 2
    if mode == 2:
        if counter < 30:
            active_frame = 2
        if 30 <= counter < 60:
            active_frame = 1
    counter += 1
    return active_frame, counter

def update_2(mode1, counter):
    active_frame = 0
    if counter >= 60:
        counter = 0
    if mode1 == 0:
        if counter < 30:
            active_frame = 0
        if 30 <= counter < 60:
            active_frame = 0
    if mode1 == 1:
        if counter < 30:
            active_frame = 1
        if 30 <= counter < 60:
            active_frame = 2
    if mode1 == 2:
        if counter < 30:
            active_frame = 2
        if 30 <= counter < 60:
            active_frame = 0
    counter += 1
    return active_frame, counter

# Printing statements
def printstat(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    back_g.blit(img, (x, y))

def display_game_over(winner):
    back_g.fill((0, 0, 0))
    game_over_text = "Game Over"
    if winner == 1:
        winner_text = "Player 1 Wins"
    else:
        winner_text = "Player 2 Wins"
    printstat(game_over_text, text_font, white, 180, 150)
    printstat(winner_text, player_font, white, 280, 250)
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()
    exit()

# Game Loop
while not game_exit and not game_over:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                mode = 1
                mode1 = 1
            if event.key == pygame.K_LEFT:
                mode = 2
                mode1 = 2
            if event.key == pygame.K_UP:
                mode = 0
                mode1 = 0
            if event.key == pygame.K_DOWN:
                mode = 0
                mode1 = 0
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                mode = 0
                mode1 = 0
        if mode == 1:
            if px1 + xspeed < 700:
                rx += xspeed
                px1 += xspeed
            if px2 + xspeed < 350:
                rex += xspeed
                px2 += xspeed
        elif mode == 2:
            if px1 - xspeed > 350:
                rx -= xspeed
                px1 -= xspeed
            if px2 - xspeed > 0:
                rex -= xspeed
                px2 -= xspeed


    # Fitting the image in the game window
    scaled_img = pygame.transform.scale(back_img, (750, 500))
    scaled_img1=pygame.transform.scale(tug_of_war,(500,150))

    # Blit the background image onto the display surface every frame
    back_g.blit(scaled_img, (0, 0))
    back_g.blit(scaled_img1,(120,12))

    # Title and Player Info
    printstat("Player 1", player_font, white, 120, 400)
    printstat("Player 2", player_font, white, 500, 400)

    # Margin
    pygame.draw.line(back_g, green, [380, 175], [380, 500], 10)

    # Rope
    pygame.draw.line(back_g, brown, [rx, ry], [rex, rey], 5)

    # Updating frames for animation
    active_frame, counter = update_1(mode, counter)
    char1 = pygame.image.load(char1_frame[active_frame]).convert_alpha()
    back_g.blit(char1, (px1, py1))

    active_frame2, counter = update_2(mode1, counter)
    char2 = pygame.image.load(char2_frame[active_frame2]).convert_alpha()
    back_g.blit(char2, (px2, py2))
    # Check for Game Over
    if px1 < 370:
        display_game_over(1)  # Player 2 wins
    if px2 > 340:
        display_game_over(2)  # Player 1 wins
    # Update the display
    pygame.display.update()
pygame.quit()