import pygame
import os
import math

pygame.init()

pygame.font.init()#INITALLIZING FONTS
pygame.mixer.init()#INITIALLIZING MIXER FOR MUSIC

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("PONG")

#~~~~~~~~~~MUSIC ELEMENTS~~~~~~~~~~

pygame.mixer.music.load(os.path.join("assets","pongmusic.mp3"))
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.1)

pygame.display.set_icon(screen)
score_val = 0
font = pygame.font.Font("assets/pixel.ttf", 20)
font2 = pygame.font.Font("assets/pixel.ttf", 30)

player1_x = 560
player1_y = 200
player1_y_change = 0

player2_x = 30
player2_y = 200

ball_x = 300
ball_y = 200
ball_x_change = 0.06
ball_y_change = -0.06


def player1(x, y):
    pygame.draw.rect(screen, (255, 255, 255), (x, y, 15, 50))


def player2(x, y):
    pygame.draw.rect(screen, (255, 255, 255), (x, y, 15, 50))


def ball(x, y):
    pygame.draw.rect(screen, (0, 0, 255), (x, y, 15, 15))


def collision(x1, y1, x2, y2):
    dist = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if dist <= 30:

        return True
    else:
        return False


def show_score(x):
    score = font.render("SCORE: " + str(x), True, (255, 255, 255))
    screen.blit(score, (250, 0))


def game_over():
    over_1 = font2.render("GAME OVER", True, (255, 0, 0))
    over_2 = font.render("PRESS SPACEBAR TO TRY AGAIN", True, (0, 255, 0))

    screen.blit(over_1, (200, 150))
    screen.blit(over_2, (100, 200))


run = True
while run:

    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                player1_y_change = -0.1

            if event.key == pygame.K_DOWN:
                player1_y_change = 0.1

            if event.key == pygame.K_SPACE:
                ball_x = 300
                score_val=0

    player1_y += player1_y_change
    player2_y += ball_y_change

    ball_x += ball_x_change
    ball_y += ball_y_change

    collide1 = collision(player1_x, player1_y, ball_x, ball_y)
    if collide1:

        ball_x_change = -0.06


    collide2 = collision(player2_x, player2_y, ball_x, ball_y)
    if collide2:
        score_val += 5

        ball_x_change = 0.06

    if player1_y >= 330 or player1_y <= 20:
        player1_y_change = 0

    if ball_y <= 20:
        ball_y_change = 0.06

    if ball_y >= 330:
        ball_y_change = -0.06

    if ball_x >= 560 or ball_x <= 20:
        game_over()
        ball_x = 650

    player1(player1_x, player1_y)
    player2(player2_x, player2_y)
    ball(ball_x, ball_y)
    show_score(score_val)
    pygame.display.update()
