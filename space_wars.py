import pygame
import os
import time 
import random

pygame.font.init()#INITALLIZING FONTS
pygame.mixer.init()#INITIALLIZING MIXER FOR MUSIC

width,height=700,500
velocity=5
var=pygame.display.set_mode((width,height))
pygame.display.set_caption("SPACE_WARS")

#~~~~~~~~~~IMAGE ELEMENTS~~~~~~~~~~

space_ship=pygame.transform.scale(pygame.image.load(os.path.join("assets","rocket.png")),(70,50))#loading assets
space_ship_bullet=pygame.transform.scale(pygame.image.load(os.path.join("assets","rocket_bullet.png")),(10,60))#loading assets

enemy_ship_yellow=pygame.transform.scale(pygame.image.load(os.path.join("assets","enemy_yellow.png")),(70,50))#loading assets
enemy_ship_green=pygame.transform.scale(pygame.image.load(os.path.join("assets","enemy_green.png")),(70,50))#loading assets
green_enemy_bullet=pygame.transform.scale(pygame.image.load(os.path.join("assets","green_bullet.png")),(10,60))#loading assets
yellow_enemy_bullet=pygame.transform.scale(pygame.image.load(os.path.join("assets","yellow_bullet.png")),(10,60))#loading assets

bg=pygame.transform.scale(pygame.image.load(os.path.join("assets","bg1s.png")),(width,height))#loading bg
title=pygame.transform.scale(pygame.image.load(os.path.join("assets","space_war_bg.png")),(width,height))#loading bg

#~~~~~~~~~~MUSIC ELEMENTS~~~~~~~~~~

pygame.mixer.music.load(os.path.join("assets","bg_sound_Spookie.mp3"))
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.1)

bullet_fx = pygame.mixer.Sound(os.path.join("assets","laser_shot.mp3"))
explosion_fx =  pygame.mixer.Sound(os.path.join("assets","explosion_sound.mp3"))

class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)

    def draw(self,window):
        var.blit(self.img,(self.x,self.y))

    def move (self,velocity):
        self.y +=velocity

    def off_screen(self,height):
        return not(self.y <= height and self.y>=0)
    
    def collision(self,obj):
        return collide(self,obj)


class ship:
    COOLDOWN=20
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.ship_img=None
        self.laser_img=None
        self.lasers=[]
        self.cool_down_counter=0#wait for half second before shooting another laser

    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,velocity,obj):#hit player
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health-=10#player
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter>=self.COOLDOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter>0:
            self.cool_down_counter+=1

    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x+30, self.y, self.laser_img)#position of the laser and image
            self.lasers.append(laser)
            self.cool_down_counter=1

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

class Player(ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img=space_ship
        self.laser_img=space_ship_bullet
        self.mask=pygame.mask.from_surface(self.ship_img)
        self.max_health=health

    def move_lasers(self,velocity,objs):#hit enemy
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        explosion_fx.play()
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y+self.ship_img.get_height()+10,(self.ship_img.get_width()*self.health/self.max_health),10))
        #green bar to show player health


class Enemy(ship):
    color_map={
            "green":(enemy_ship_green,green_enemy_bullet),
            "yellow":(enemy_ship_yellow,yellow_enemy_bullet)
            }
    def __init__(self, x, y,color, health=100):
        super().__init__(x, y, health)
        self.ship_img,self.laser_img=self.color_map[color]
        self.mask=pygame.mask.from_surface(self.ship_img)


    def move(self,velocity):
        self.y+=velocity

    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x+30, self.y, self.laser_img)#position of laser and image 
            self.lasers.append(laser)
            self.cool_down_counter=1

def movement(key_press,player):
    if key_press[pygame.K_LEFT] and player.x-velocity>0 :
        player.x-=velocity
    if key_press[pygame.K_RIGHT] and player.x+velocity+player.get_width()<width :
        player.x+=velocity
    if key_press[pygame.K_SPACE]:
        player.shoot()
        bullet_fx.play()

def collide(obj1,obj2):
    offset_x=obj2.x-obj1.x
    offset_y=obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) !=None 


def main():
    player=pygame.Rect(400,350,70,50)
    fps=60
    clock=pygame.time.Clock()
    run = True
    lost=False
    lost_count=5
    level=0
    lives=10
    main_font=pygame.font.SysFont("comicsans",20)
    lost_font=pygame.font.SysFont("comicsans",60)
    enemies=[]
    wave_length=5
    enemy_vel=2
    laser_vel=10
    player=Player(400,400)#spwans the player

    def redraw_window():
        var.blit(bg,(0,0))
        #var.blit(space_ship,(player.x,player.y))#draw surface on the screen
        level_label=main_font.render(f"LEVEL: {level}",1,(255,0,0))
        lives_label=main_font.render(f"LIVES: {lives}",1,(255,0,0))
        
        var.blit(level_label,(50,10))
        var.blit(lives_label,(550,10))

        player.draw(var)
        
        for enemy in enemies:#enemy
            enemy.draw(var)

        if lost==True:
            lost_label=lost_font.render("GAME OVER!!!",1,(255,0,0))
            var.blit(lost_label,(width/2 - lost_label.get_width()/2, 250))
        
        pygame.display.update()

    while run:
        clock.tick(fps)#THIS CONTROLLS THE WHILE LOOp
        redraw_window()

        if lives<=0 or player.health<=0:
            lost=True
            lost_count+=1

        if lost:
            if lost_count > fps*3:
                run=False
            else:
                continue

        if len(enemies)==0:
            level+=2
            wave_length+=5
            for i in range(wave_length):
                enemy=Enemy(random.randrange(50,width-100),random.randrange(-1500,-100),random.choice(["yellow","green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False    
        
        key_press=pygame.key.get_pressed()
        movement(key_press,player)

        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)

            if random.randrange(0,2*60) == 1:#60 times 2 
                enemy.shoot()

            if collide(enemy,player):
                player.health-=10
                enemies.remove(enemy)

            elif enemy.y+enemy.get_height()>height:
                lives-=1
                enemies.remove(enemy)

            
        player.move_lasers(-laser_vel, enemies)#negative velocity for laser to go up
        

def main_menu():
    title_font=pygame.font.SysFont("comicsans",30)
    instr1_font=pygame.font.SysFont("Times New Roman",30)
    instr2_font=pygame.font.SysFont("Times New Roman",30)

    run=True
    while run:#infinte loop
        var.blit(title, (0,0))
        title_label=title_font.render("Press the mouse to begin...",1,(255,255,255))
        var.blit(title_label,(width/2 - title_label.get_width()/2,400))
        instr1_label=instr1_font.render("Press SPACE BAR to Shoot",1,(255,255,255))
        instr2_label=instr2_font.render("Press < and > KEYS to move Around",1,(255,255,255))
        var.blit(instr1_label,(width/2 - instr1_label.get_width()/2,290))
        var.blit(instr2_label,(width/2 - instr2_label.get_width()/2,320))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type ==  pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

if __name__==main_menu():
    main_menu()