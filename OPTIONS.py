import pygame
import main

def options():
    drawOptions()
    pygame.display.update()
    while main.run and not main.runMenu:
        main.clock.tick(main.FPS)

        if main.musicSlider.update():
            drawOptions()
            pygame.mixer.music.set_volume(main.musicSlider.value)

        if main.soundSlider.update():
            drawOptions()
            main.shootingSound.set_volume(main.soundSlider.value)
            main.shipExplosionSound.set_volume(main.soundSlider.value)
            main.asteroidExplosionSound.set_volume(main.soundSlider.value)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main.runMenu = True

        pygame.display.update()
def drawOptions():
    main.win.blit(main.imageBg, (0, 0))
    main.musicSlider.draw(main.win)
    main.soundSlider.draw(main.win)