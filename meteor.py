import pygame
import main

class Meteor:
    def __init__(self,x,y,multiplier):
        self.image = pygame.transform.scale(main.METEOR_IMAGE,(84+multiplier*2-10,68+multiplier*2-10))
        self.x = x
        self.y = y
        self.vel = 6
        self.multiplier = multiplier
        self.hitbox = (self.x + 6, self.y + 6, 80+multiplier*2-10, 62+multiplier*2-10)
        self.health = self.multiplier
    
    def draw(self, surface):
        if main.run:
            surface.blit(self.image,(self.x,self.y))
            self.hitbox = pygame.Rect(self.x + 6, self.y + 6, 80+self.multiplier*2-10, 62+self.multiplier*2-10)
            pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)

    def takeDmg(self):
        self.health -= main.shipDmg
        return self.health<=0

