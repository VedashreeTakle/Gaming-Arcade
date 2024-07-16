import pygame
import os
from subprocess import call

pygame.init()  # Initialize Pygame
pygame.font.init()#INITALLIZING FONTS
pygame.mixer.init()#INITIALLIZING MIXER FOR MUSIC

width,height=700,500
var=pygame.display.set_mode((width,height))
pygame.display.set_caption("ARCADE")

colour=(10,10,30)
green=(0,200,0)
fps = 60#UPDATE GAME PER SECONDS OF FRAME
velocity=5

#images**************
arc1=pygame.transform.scale(pygame.image.load(os.path.join("assets","arcade1.png")),(70,180))
arc2=pygame.transform.scale(pygame.image.load(os.path.join("assets","arc2.png")),(70,150))
arc3=pygame.transform.scale(pygame.image.load(os.path.join("assets","arcade4.png")),(70,150))
arc4=pygame.transform.scale(pygame.image.load(os.path.join("assets","arc4.png")),(70,150))
back_img=pygame.image.load(os.path.join("assets","arcade_bg.jpg"))

#~~~~~~~~~~MUSIC ELEMENTS~~~~~~~~~~

pygame.mixer.music.load(os.path.join("assets","jazz_music_aracde.mp3"))
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.1)

class Button:
    def __init__(self, x, y, image, scale):
        width = arc1.get_width()
        height = arc1.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        var.blit(self.image, self.rect)  # Corrected blitting
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                pygame.mixer.music.stop()

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action
   

arc1_button = Button(100,200, arc1,1)  # Load the image within the Button class
arc2_button = Button(250,200, arc2,1)  # Load the image within the Button class
arc3_button = Button(400,200, arc3,1)  # Load the image within the Button class
arc4_button = Button(550,200, arc4,1)  # Load the image within the Button class

game_exit=False

title_font=pygame.font.SysFont("comicsans",15)


while not game_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
            
    scaled_img=pygame.transform.scale(back_img,(750,500))
    var.blit(scaled_img,(0,0))
    #var.blit(arc1,(225,250))
    title1=title_font.render("TUG OF WAR",1,(255,255,255))
    var.blit(title1,(90,380))
    title2=title_font.render("SPACE WARS",1,(255,255,255))
    var.blit(title2,(240,380))
    title3=title_font.render("CAR RACING",1,(255,255,255))
    var.blit(title3,(400,380))
    title4=title_font.render("PONG",1,(255,255,255))
    var.blit(title4,(550,380))
    if arc1_button.draw()==True:
        call(["python","start.py"])
    if arc2_button.draw()==True:
        call(["python","space_wars.py"])
    if arc3_button.draw()==True:
        call(["python","car_race.py"])
    if arc4_button.draw()==True:
        call(["python","pong.py"])


    pygame.display.update()

pygame.quit()
