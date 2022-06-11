import pygame

class Text:
    def __init__(self,x,y,name,size,color,outlines):
        self.x=x
        self.y=y
        self.name=name
        self.size = size
        self.color = color
        self.outlines = outlines
        self.timesDrawn = 0
    def draw(self,surface):
        font = pygame.font.Font('freesansbold.ttf', self.size)
        text = font.render(self.name, True, self.color)
        textOutline = font.render(self.name, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.x,self.y)
        outlineWidth = self.size/20
        self.timesDrawn += 1

        # textOutline
        if self.outlines:
            surface.blit(textOutline, (textRect.x - outlineWidth, textRect.y + outlineWidth))
            surface.blit(textOutline, (textRect.x - outlineWidth, textRect.y - outlineWidth))
            surface.blit(textOutline, (textRect.x + outlineWidth, textRect.y + outlineWidth))
            surface.blit(textOutline, (textRect.x + outlineWidth, textRect.y - outlineWidth))
        # text
        surface.blit(text, textRect)

    def updateName(self,name):
        self.name = name
    def updatePos(self,x,y):
        self.x = x
        self.y = y
