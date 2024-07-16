import pygame
from subprocess import call

pygame.init()  # Initialize Pygame

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 500
game_exit = False
game_over = False
sound = pygame.mixer.Sound("game sound.mp3")
sound.play()
sound.set_volume(0.2)
back_ground = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tug of War")

start_img = pygame.image.load("start image.jpg").convert_alpha()
back_img=pygame.image.load("grass.png").convert_alpha()
tug_of_war=pygame.image.load("tug of war title.jpg").convert_alpha()



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
   

start_button = Button(225,250, start_img,1)  # Load the image within the Button class

while not game_exit and not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True

    scaled_img=pygame.transform.scale(back_img,(750,500))
    scaled_img1=pygame.transform.scale(tug_of_war,(500,150))
    back_ground.blit(scaled_img,(0,0))
    back_ground.blit(start_img,(225,250))
    back_ground.blit(scaled_img1,(120,25))
    if start_button.draw()==True:
        call(["python","tugofwar.py"])


    pygame.display.update()

pygame.quit()
