import main
from random import randint, randrange
import pygame

class Enemy:
    def __init__(self, x, y, multiplier):
        self.x = x
        self.y = y
        self.speed_x = 5
        self.speed_y = 4
        self.width = 126
        self.height = 66
        self.image = main.ENEMY_IMAGE
        self.direction = -1
        self.vel = 3
        self.multiplier = multiplier
        self.rect = pygame.Rect(x, y, 50, 50)
        self.hitbox = (self.rect.x + 15, self.rect.y + 15, 90, 45)
        self.health = self.multiplier

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x + 15, self.y + 15, 90, 45)
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)

    def takeDmg(self):
        self.health -= main.shipDmg
        return self.health <= 0
