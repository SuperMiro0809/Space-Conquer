import pygame
import main

def fadeOut():
    fadeout = pygame.Surface((main.WIDTH, main.HEIGHT))
    fadeout = fadeout.convert()
    fadeout.fill((0,0,0))
    for i in range(255):
        fadeout.set_alpha(i)
        main.win.blit(fadeout, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.run = False
        if main.run == False:
            break

