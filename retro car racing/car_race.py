import pygame
from subprocess import call

pygame.init()  # Initialize Pygame

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
game_exit = False
game_over = False
sound = pygame.mixer.Sound("assets/carracemusic.mp3")
sound.play(loops=-1)
sound.set_volume(0.2)
back_ground = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Race")

start_img = pygame.transform.scale(pygame.image.load("assets/Start-button.png").convert_alpha(),(180,150))
back_img=pygame.image.load("assets/car_race_bg.png").convert_alpha()
race=pygame.image.load("assets/race_tit.jpg").convert_alpha()


class Button:
    def __init__(self, x, y, image, scale):
        width = start_img.get_width()
        height = start_img.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        back_ground.blit(self.image, self.rect)  # Corrected blitting
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action
   

start_button = Button(80,280, start_img,1)  # Load the image within the Button class

while not game_exit and not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True

    scaled_img=pygame.transform.scale(back_img,(750,500))
    scaled_img1=pygame.transform.scale(race,(450,130))
    back_ground.blit(scaled_img,(0,0))
    back_ground.blit(start_img,(80,280))
    back_ground.blit(scaled_img1,(120,25))
    if start_button.draw()==True:
        call(["python","car.py"])


    pygame.display.update()

pygame.quit()
