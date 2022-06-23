import pygame
import main

class Spaceship():
    def __init__(self,x,y):
        self.image = main.SPACESHIP_IMAGE
        self.exhaust_image = main.SPACESHIP_EXHAUST_IMAGE
        self.movex = 0
        self.movey = 0
        self.width = 84
        self.height = 84
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.hitbox = (self.rect.x, self.rect.y + 20, 84, 41)

    def resetPos(self,surface):
        self.movex = 0
        self.movey = 0
        main.win.blit(main.imageBg, (0, 0))
        self.rect.centerx = 0 - self.width
        self.rect.centery = main.HEIGHT//2
        surface.blit(self.image,(self.rect.x,self.rect.y))
        surface.blit(self.exhaust_image, (self.rect.x - 30, self.rect.y + 26))
        pygame.display.update()

        for i in range(main.WIDTH//8):
            main.clock.tick(main.FPS)
            main.win.blit(main.imageBg, (0, 0))
            main.stageText.draw(main.win)
            self.rect.centerx+=2
            self.draw(surface)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main.run = False
            if main.run == False:
                break


    def draw(self, surface):
        surface.blit(self.image,(self.rect.x,self.rect.y))
        surface.blit(self.exhaust_image,(self.rect.x - 30,self.rect.y + 26))
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y + 20, 84, 41)
    
    def movement(self, keys_pressed):


        if keys_pressed == pygame.K_d and self.rect.x + main.shipSpeed//5 + 3 < main.WIDTH:  #right
            self.movex += main.shipSpeed//5 + 3
            if self.movex == 0:
                self.movex +=main.shipSpeed//5 + 3
        if keys_pressed == pygame.K_a and self.rect.x - 32 - main.shipSpeed//5 + 3 > 0:  #left
            self.movex -= main.shipSpeed//5 + 3
            if self.movex == 0:
                self.movex -=main.shipSpeed//5 + 3
        if keys_pressed == pygame.K_w and self.rect.y - main.shipSpeed//5 + 3 > 0:  #up
            self.movey -= main.shipSpeed//5 + 3
            if self.movey == 0:
                self.movey -=main.shipSpeed//5 + 3
        if keys_pressed == pygame.K_s and self.rect.y + main.shipSpeed//5 + 3 < main.HEIGHT - 84:  #down
            self.movey += main.shipSpeed//5 + 3
            if self.movey == 0:
                self.movey +=main.shipSpeed//5 + 3

    
    def stop(self, keys_pressed):
        if keys_pressed == pygame.K_d and self.movex>0:  # right
            self.movex = 0
        if keys_pressed == pygame.K_a and self.movex<0:  # left
            self.movex = 0
        if keys_pressed == pygame.K_w and self.movey<0:  # up
            self.movey = 0
        if keys_pressed == pygame.K_s and self.movey>0:  # down
            self.movey = 0
    
    def update(self, bullets):
        if self.rect.x + self.movex > main.WIDTH - 84 or self.rect.x + self.movex < 0:
            self.movex = 0
        if self.rect.y + self.movey > main.HEIGHT - 64 or self.rect.y + self.movey < 0 - 22:
            self.movey = 0
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        for bullet in bullets:
            bullet.draw()

class Projectile():
    def __init__(self,x,y, surface):
        self.image = pygame.transform.scale(main.PROJECTILE_IMAGE,(64,64))
        self.x = x
        self.y = y
        self.surface = surface
        self.vel = 8
    
    def draw(self):
        self.surface.blit(self.image,(self.x-18,self.y-17))
        self.hitbox = pygame.Rect(self.x, self.y+8, 32, 16)
