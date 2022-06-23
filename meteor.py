import pygame
import main


class Meteor:
    def __init__(self, x, y, multiplier):
        self.width = 84 + multiplier * 2 - 10
        self.height = 68 + multiplier * 2 - 10
        self.image = pygame.transform.scale(main.METEOR_IMAGE, (self.width, self.height))
        self.x = x
        self.y = y
        self.vel = 3
        self.multiplier = multiplier
        self.hitbox = (self.x + 6, self.y + 6, self.width, self.height)
        self.health = self.multiplier

    def draw(self, surface):
        if main.run:
            surface.blit(self.image, (self.x, self.y))
            self.hitbox = pygame.Rect(self.x, self.y,self.width,self.height)

    def takeDmg(self):
        self.health -= main.shipDmg
        return self.health <= 0
