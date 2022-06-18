import pygame
import main
from textWithOutline import Text

class moneyEarned:
    def __init__(self,value,timer,x,y):
        self.value = value
        self.timer = timer
        self.x = x
        self.y = y
        self.text = Text(self.x,self.y,f"+{self.value}$",30,(46, 120, 40), True)
    def draw(self,surface):
        self.text.draw(surface)
        self.y -= 1
        self.text.updatePos(self.x,self.y)
        self.timer -= 1
        return self.timer < 0

class asteroidExplosion:
    def __init__(self,timeBetween,x,y,size):
        self.explosionStage = 1
        self.timeBetween = timeBetween
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load('Assets/explosions/Explosion1.png'), (32*self.size, 32*self.size))
        self.x = x - self.size*16
        self.y = y - self.size*16
        self.timer = 0
    def draw(self,surface):
        surface.blit(self.image,(self.x,self.y))
        self.timer+=1
        if self.timer == self.timeBetween:
            self.timer = 0
            self.explosionStage += 1
            if self.explosionStage<=8:
                self.image = pygame.transform.scale(pygame.image.load(f'Assets/explosions/Explosion{self.explosionStage}.png'), (32*self.size, 32*self.size))
                return False
            else:
                return True
        return False
class bulletExplosions:
    def __init__(self):
