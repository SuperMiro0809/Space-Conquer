import pygame
import json
import os.path
import main
from GAME import game
from fade import fadeOut

def menu():
    drawMenu()
    while main.run and main.runMenu:
        main.clock.tick(main.FPS)
        if main.PLAY_BUTTON.check():
            start()
            main.runMenu = False
            main.runGame = True
            fadeOut()
            game()
            if main.run:
                drawMenu()
        elif main.LOAD_BUTTON.check():
            load()
            main.runMenu = False
            main.runGame = True
            game()
            if main.run:
                drawMenu()
        elif main.EXIT_BUTTON.check():
            main.run = False


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.run = False
    if main.shipDmg!=0:
        main.generateFile()
    main.win.fill((0,0,0))

def drawMenu():
    main.win.blit(main.imageBg, (0, 0))
    if os.path.exists('data_save.txt'):
        main.PLAY_BUTTON.rect.center = (main.WIDTH / 2, main.startBtnHeight + 30)
        main.LOAD_BUTTON.draw(main.win)
    else:
        main.PLAY_BUTTON.rect.center = (main.WIDTH / 2, (main.startBtnHeight + 30) * 2)
    main.PLAY_BUTTON.draw(main.win)
    main.EXIT_BUTTON.draw(main.win)

def load():
    if os.path.exists('data_save.txt'):
        with open('data_save.txt') as data_save_file:
            data = json.load(data_save_file)
            main.shipSpeed = data['shipSpeed']
            main.shipDmg = data['shipDmg']
            main.attackSpeed = data['attackSpeed']
            main.shipHealth = data['shipHealth']
            main.money = data['money']
            main.stage = data['stage']

def start():
    main.shipSpeed = 3
    main.shipDmg = 1
    main.attackSpeed = 1
    main.shipHealth = 1
    main.money = 1000
    main.stage = 1