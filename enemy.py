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
        self.previous_time = pygame.time.get_ticks() - 1000
        self.attackSpeed = 0.5 * main.stage
        self.direction = randint(0, 1)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x + 15, self.y + 15, 90, 45)
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.direction == 0:
            if self.y + self.vel <= main.HEIGHT - self.height: 
                self.y += self.vel
            else:
                self.direction = 1
        else:
            if self.y - self.vel >= 0:
                self.y -= self.vel
            else:
                self.direction = 0
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.previous_time > 1000 / self.attackSpeed:
            self.previous_time = current_time
            main.enemyBullets.append(EnemyProjectile(round(self.x - self.width // 2 + 40),round(self.y + 25), main.win))

        for bullet in main.enemyBullets:
            bullet.draw()

    def takeDmg(self):
        self.health -= main.shipDmg
        return self.health <= 0

class EnemyProjectile():
    def __init__(self,x,y, surface):
        self.image = main.ENEMY_PROJECTILE_IMAGE
        self.x = x
        self.y = y
        self.surface = surface
        self.vel = 8
    
    def draw(self):
        self.surface.blit(self.image,(self.x,self.y))
        self.hitbox = pygame.Rect(self.x, self.y+8, 32, 16)
        pygame.draw.rect(main.win, (255, 0, 0), self.hitbox, 2)
