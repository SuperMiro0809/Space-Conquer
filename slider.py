import pygame
from textWithOutline import Text


class SLIDER():
    def __init__(self,surface,name,x,y,width,value):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = 5
        self.circlex = x - width/2 + value*width
        self.circley = (self.height // 2 + y)-2
        self.rectangle = pygame.Rect(x,y,width, self.height)
        self.rectangle.center = (x,y)
        self.outlineRect = pygame.Rect(x,y,width+6, self.height+6)
        self.outlineRect.center = (x, y)
        self.circle = [surface,(100,100,100),(self.circlex,self.circley),10]
        self.circleCollider = pygame.Rect(self.circlex-10,self.circley-10,20,20)
        self.text = Text(self.x,self.y-50,self.name,30,(255,255,255),True)
        self.value = value
        self.clicked = False

    def draw(self,screen):
        pygame.draw.rect(screen, (0, 0, 0), self.outlineRect)
        pygame.draw.rect(screen,(255,255,255),self.rectangle)
        pygame.draw.circle(self.circle[0], (0,0,0), self.circle[2], self.circle[3]+2)
        pygame.draw.circle(self.circle[0],self.circle[1],self.circle[2],self.circle[3])
        self.text.draw(screen)

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.circleCollider.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False
        elif self.clicked:
            if self.circlex != pos[0]:
                if pos[0]<self.x+self.width//2 and pos[0]>self.x-self.width//2:
                    self.circleCollider.move_ip(pos[0]-self.circlex,0)
                    self.circlex = pos[0]
                    self.circle[2] = (self.circlex,self.circley)
                elif pos[0]<=self.x-self.width//2:
                    self.circleCollider.move_ip(self.x-self.width//2 - self.circlex, 0)
                    self.circlex = self.x-self.width//2
                    self.circle[2] = (self.circlex, self.circley)
                else:
                    self.circleCollider.move_ip(self.x + self.width // 2 - self.circlex, 0)
                    self.circlex = self.x + self.width // 2
                    self.circle[2] = (self.circlex, self.circley)
                self.value = (self.circlex - self.x + self.width // 2) / self.width
                return True
        return False