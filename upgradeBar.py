import pygame
from button import Button
from textWithOutline import Text
import main

class upgrade:

    def __init__(self,level,x,y,name):
        self.level = level
        self.BarX = 1752*0.1
        self.BarY = 876*0.1
        self.img = pygame.transform.scale(pygame.image.load(f'Assets/upgradeBar/bar{level}.png'),(self.BarX,self.BarY))
        self.price = 100*level
        self.name = name
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        upgradeBtnImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/upgradeBtn.png'),(self.BarY//3,self.BarY//3))
        self.upgradeBtn = Button(x+self.BarX/1.7,y,upgradeBtnImg)

    def draw(self,surface):
        self.img = pygame.transform.scale(pygame.image.load(f'Assets/upgradeBar/bar{self.level}.png'), (self.BarX, self.BarY))
        surface.blit(self.img, (self.rect.x, self.rect.y))

        name = Text(self.rect.centerx,self.rect.centery - 40,self.name,26,(255,255,255),True)
        name.draw(surface)

        if self.level == 15:
            priceText = Text(self.rect.centerx, self.rect.centery + 40, f"MAXED", 20, (255, 255, 255), True)
        else:
            if self.price<=main.money:
                priceText = Text(self.rect.centerx,self.rect.centery + 40,f"{self.price}$",20,(50, 168, 82),True)
            else:
                priceText = Text(self.rect.centerx, self.rect.centery + 40, f"{self.price}$", 20, (145, 33, 23), True)
        priceText.draw(surface)

        self.upgradeBtn.draw(surface)

    def check(self):
        return self.upgradeBtn.check()


    def buy(self):
        if self.level<15 and main.money>=self.price:
            self.level = self.level + 1
            main.money = main.money - self.price
            self.price += 100
        return self.level