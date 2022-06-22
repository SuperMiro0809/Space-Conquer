import pygame
import json
import os.path
import main
from GAME import game,bossBattle
from fade import fadeOut
from OPTIONS import options
from skin import Skin

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
            if main.stage == 10:
                bossBattle()
            else:
                game()
            if main.run:
                drawMenu()
        elif main.EXIT_BUTTON.check():
            main.run = False
        elif main.OPTIONS_BUTTON.check():
            main.runMenu = False
            options()
            if main.run:
                drawMenu()


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.run = False
    if main.shipDmg!=0:
        main.generateFile()
    main.generateSaveOptionsFile()
    main.win.fill((0,0,0))

def drawMenu():
    main.win.blit(main.imageBg, (0, 0))
    if os.path.exists('data_save.txt'):
        main.PLAY_BUTTON.rect.center = (main.WIDTH / 2, main.startBtnHeight + 30)
        main.LOAD_BUTTON.draw(main.win)
    else:
        main.PLAY_BUTTON.rect.center = (main.WIDTH / 2, (main.startBtnHeight + 30) * 2)
    main.PLAY_BUTTON.draw(main.win)
    main.OPTIONS_BUTTON.draw(main.win)
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

            for skin in data['skins']:
                if not skin['title'] == 'Ship 1':
                    skinData = loadSkin(skin['title'])
                    s = Skin(skin['title'], skinData['image'], skinData['exhaust'], skinData['projectile'], skin['equipped'])
                    main.skins.append(s)

                    if skin['equipped']:
                        for sk in main.skins:
                            sk.equipped = False
                        main.selectedSkin = s
                        main.SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load(main.selectedSkin.image), (84, 84))
                        main.SPACESHIP_EXHAUST_IMAGE = pygame.transform.scale(pygame.image.load(main.selectedSkin.exhaust), (32, 32))
                        main.PROJECTILE_IMAGE = pygame.transform.scale(pygame.image.load(main.selectedSkin.projectile), (32, 32))

def loadSkin(skin):
    shipObj = { 'image': '', 'exhaust': '', 'projectile': '' }

    if skin == 'Ship 2':
        shipObj['image'] = main.ship2SkinImage
        shipObj['exhaust'] = main.ship2ExhaustImage
        shipObj['projectile'] = main.ship2ProjectileImage
    elif skin == 'Ship 3':
        shipObj['image'] = main.ship3SkinImage
        shipObj['exhaust'] = main.ship3ExhaustImage
        shipObj['projectile'] = main.ship3ProjectileImage
    elif skin == 'Ship 4':
        shipObj['image'] = main.ship4SkinImage
        shipObj['exhaust'] = main.ship4ExhaustImage
        shipObj['projectile'] = main.ship4ProjectileImage
    elif skin == 'Ship 5':
        shipObj['image'] = main.ship5SkinImage
        shipObj['exhaust'] = main.ship5ExhaustImage
        shipObj['projectile'] = main.ship5ProjectileImage
    elif skin == 'Ship 6':
        shipObj['image'] = main.ship6SkinImage
        shipObj['exhaust'] = main.ship6ExhaustImage
        shipObj['projectile'] = main.ship6ProjectileImage

    return shipObj

def start():
    main.shipSpeed = 3
    main.shipDmg = 1
    main.attackSpeed = 1
    main.shipHealth = 1
    main.money = 1000
    main.stage = 1
