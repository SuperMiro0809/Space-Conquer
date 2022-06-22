import pygame
import main
from random import randint

class BOSS():
    def __init__(self,x,y,width,height):
        self.frame = 4
        self.height = height
        self.width = width
        self.x = x - self.width//2
        self.y = y - self.height//2
        self.vel = 1
        self.hitbox1 = pygame.Rect(self.x+20,self.y+30,self.width//2,self.height-60)
        self.hitbox2 = pygame.Rect(self.x+self.width//2,self.y+15,self.width//2,self.height//2)
        self.bring = False
        self.image = pygame.transform.scale(pygame.image.load(f'Assets/bossSprites/Boss{self.frame//4}.png'),(self.width, self.height))

    def bringBoss(self):
        self.bring = True
        self.moveX = -170
        self.moveY = 0

    def update(self):
        #change image every frame
        self.frame+=1
        if self.frame == 13:
            self.frame = 4
        self.image = pygame.transform.scale(pygame.image.load(f'Assets/bossSprites/Boss{self.frame//4}.png'),(self.width, self.height))

        if self.bring:
            if self.moveX != 0:
                self.x -= self.vel
                self.hitbox1.move_ip(-self.vel , 0)
                self.hitbox2.move_ip(-self.vel, 0)
                self.moveX+=1
            else:
                self.bring = False
        else:
            #move y
            if self.moveY > 0:
                if self.y + self.vel + self.height > main.HEIGHT:
                    self.moveY = 0
                else:
                    self.y += self.vel
                    self.hitbox1.move_ip(0 , self.vel)
                    self.hitbox2.move_ip(0 , self.vel)
                    self.moveY -= self.vel
            elif self.moveY < 0:
                if self.y - self.vel < 0:
                    self.moveY = 0
                else:
                    self.y -= self.vel
                    self.hitbox1.move_ip(0 , -self.vel)
                    self.hitbox2.move_ip(0 , -self.vel)
                    self.moveY += self.vel
            else:
                self.moveY = randint(100,300) * randint(-1,1)

    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox1, 2)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox2, 2)



