import pygame
import main
from random import randint

class BOSS():
    def __init__(self,x,y,width,height):
        self.frame = 4
        self.height = height
        self.width = width
        self.x = x - self.width//2 + self.width//2
        self.y = y - self.height//2
        self.vel = 1
        self.hitbox1 = pygame.Rect(self.x+20,self.y+30,self.width//2,self.height-60)
        self.hitbox2 = pygame.Rect(self.x+self.width//2,self.y+15,self.width//2,self.height//2)
        self.bring = False
        self.retreat = False
        self.image = pygame.transform.scale(pygame.image.load(f'Assets/bossSprites/Boss{self.frame//4}.png'),(self.width, self.height))
        self.health = 5000
        self.healthSkull = pygame.transform.scale(pygame.image.load('Assets/bossSprites/healthSkull.png'),(32,32))
        self.healthBackground = pygame.Rect(self.x+10,self.y-20,self.width - 10,16)
        self.displayedHealth = pygame.Rect(self.x+16,self.y-16,self.width - 20,8)

    def bringBoss(self):
        self.bring = True
        self.moveX = -190
        self.moveY = 0

    def update(self):
        #change image every frame
        self.frame+=1
        if self.frame == 13:
            self.frame = 4
        self.image = pygame.transform.scale(pygame.image.load(f'Assets/bossSprites/Boss{self.frame//4}.png'),(self.width, self.height))

        if self.bring:
            if self.moveX != 0:
                self.x -= self.vel*2
                self.hitbox1.move_ip(-self.vel*2 , 0)
                self.hitbox2.move_ip(-self.vel*2, 0)
                self.healthBackground.move_ip(-self.vel*2, 0)
                self.displayedHealth.move_ip(-self.vel*2, 0)
                self.moveX+=1
            else:
                self.bring = False
        elif self.retreat:
            if self.moveX != 0:
                self.x += self.vel*2
                self.hitbox1.move_ip(self.vel*2 , 0)
                self.hitbox2.move_ip(self.vel*2, 0)
                self.healthBackground.move_ip(self.vel*2, 0)
                self.displayedHealth.move_ip(self.vel*2, 0)
                self.moveX-=1
            else:
                main.gameWon = True
        else:
            #move y
            if self.moveY > 0:
                if self.y + self.vel + self.height > main.HEIGHT:
                    self.moveY = 0
                else:
                    self.y += self.vel
                    self.hitbox1.move_ip(0 , self.vel)
                    self.hitbox2.move_ip(0 , self.vel)
                    self.healthBackground.move_ip(0, self.vel)
                    self.displayedHealth.move_ip(0, self.vel)
                    self.moveY -= self.vel
            elif self.moveY < 0:
                if self.y - self.vel < 0:
                    self.moveY = 0
                else:
                    self.y -= self.vel
                    self.hitbox1.move_ip(0 , -self.vel)
                    self.hitbox2.move_ip(0 , -self.vel)
                    self.healthBackground.move_ip(0 , -self.vel)
                    self.displayedHealth.move_ip(0, -self.vel)
                    self.moveY += self.vel
            else:
                self.moveY = randint(100,300) * randint(-1,1)

    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox1, 2)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox2, 2)
        pygame.draw.rect(screen, (0, 0, 0), self.healthBackground)
        pygame.draw.rect(screen, (255, 0, 0), self.displayedHealth)
        screen.blit(self.healthSkull, (self.x-16, self.y-30))

    def takeDamage(self):
        self.health -= main.shipDmg
        self.displayedHealth = pygame.Rect(self.x+16,self.y-16,(self.width - 20) * self.health // 5000,8)
        if self.health < 0:
            self.retreatBoss()

    def retreatBoss(self):
        self.retreat = True
        self.moveX = 190
        self.moveY = 0




