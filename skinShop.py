import pygame
import main
from upgradeBar import upgrade
from fade import fadeOut
from textWithOutline import Text
from skin import Skin
import shop as upgradeShop

offCenterX = 150
offCenterY = 70


def shop():
    drawShop()
    while main.run and not main.runGame:
        main.clock.tick(main.FPS)
        
        if main.BACK_SHOP_BUTTON.check():
            upgradeShop.shop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                if main.ship1Item.collidepoint(pos):
                    skin = next((skin for skin in main.skins if skin.title == 'Ship 1'), None)
                    equipSkin(skin)
                    updateShop()
                if main.ship2Item.collidepoint(pos):
                    skin = next((skin for skin in main.skins if skin.title == 'Ship 2'), None)
                    if skin == None:
                        if main.money - 1000 >= 0:
                            main.money -= 1000
                            main.skins.append(Skin('Ship 2', main.ship2SkinImage, main.ship2ExhaustImage, main.ship2ProjectileImage, False))
                    else:
                        equipSkin(skin)
                    
                    updateShop()
                if main.ship3Item.collidepoint(pos):
                    skin = next((skin for skin in main.skins if skin.title == 'Ship 3'), None)
                    if skin == None:
                        if main.money - 1000 >= 0:
                            main.money -= 1000
                            main.skins.append(Skin('Ship 3', main.ship3SkinImage, main.ship3ExhaustImage, main.ship3ProjectileImage, False))
                    else:
                        equipSkin(skin)

                    updateShop()
                if main.ship4Item.collidepoint(pos):
                    skin = next((skin for skin in main.skins if skin.title == 'Ship 4'), None)
                    if skin == None:
                        if main.money - 1000 >= 0:
                            main.money -= 1000
                            main.skins.append(Skin('Ship 4', main.ship4SkinImage, main.ship4ExhaustImage, main.ship4ProjectileImage, False))
                    else:
                        equipSkin(skin)
                    
                    updateShop()
                if main.ship5Item.collidepoint(pos):
                    skin = next((skin for skin in main.skins if skin.title == 'Ship 5'), None)
                    if skin == None:
                        if main.money - 1000 >= 0:
                            main.money -= 1000
                            main.skins.append(Skin('Ship 5', main.ship5SkinImage, main.ship5ExhaustImage, main.ship5ProjectileImage, False))
                    else:
                        equipSkin(skin)
                    
                    updateShop()
                if main.ship6Item.collidepoint(pos):
                    skin = next((skin for skin in main.skins if skin.title == 'Ship 6'), None)
                    if skin == None:
                        if main.money - 1000 >= 0:
                            main.money -= 1000
                            main.skins.append(Skin('Ship 6', main.ship6SkinImage, main.ship6ExhaustImage, main.ship6ProjectileImage, False))
                    else:
                        equipSkin(skin)
                    
                    updateShop()       
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main.runGame = True
                    fadeOut()

def drawShop():
    main.win.blit(main.shopBg, (0, 0))
    drawShopItems()
    main.skinShopText.draw(main.win)
    main.BACK_SHOP_BUTTON.draw(main.win)

    moneyText = Text(100, 50, f"{main.money}$", 20, (46, 120, 40), True)
    moneyText.draw(main.win)

    pygame.display.update()

def updateShop():
    drawShop()
    pygame.display.update()

def drawShopItems():
    pygame.draw.rect(main.win, (72,72,72), main.ship1Item, 2)
    pygame.draw.rect(main.win, (72,72,72), main.ship2Item, 2)
    pygame.draw.rect(main.win, (72,72,72), main.ship3Item, 2)

    pygame.draw.rect(main.win, (72,72,72), main.ship4Item, 2)
    pygame.draw.rect(main.win, (72,72,72), main.ship5Item, 2)
    pygame.draw.rect(main.win, (72,72,72), main.ship6Item, 2)

    moneyTexts = [
        Text(290, 235, f"{formatText('Ship 1')}", 20, formatColor('Ship 1'), True),
        Text(490, 235, f"{formatText('Ship 2')}", 20, formatColor('Ship 2'), True),
        Text(690, 235, f"{formatText('Ship 3')}", 20, formatColor('Ship 3'), True),
        Text(290, 375, f"{formatText('Ship 4')}", 20, formatColor('Ship 4'), True),
        Text(490, 375, f"{formatText('Ship 5')}", 20, formatColor('Ship 5'), True),
        Text(690, 375, f"{formatText('Ship 6')}", 20, formatColor('Ship 6'), True),
    ]

    for moneyText in moneyTexts:
        moneyText.draw(main.win)

    main.win.blit(main.ship1Skin, (270, 150))
    main.win.blit(main.ship1Exhaust, (240, 175))

    main.win.blit(main.ship2Skin, (460, 150))
    main.win.blit(main.ship2Exhaust, (445, 175))

    main.win.blit(main.ship3Skin, (660, 150))
    main.win.blit(main.ship3Exhaust, (645, 175))

    main.win.blit(main.ship4Skin, (260, 290))
    main.win.blit(main.ship4Exhaust, (240, 315))

    main.win.blit(main.ship5Skin, (460, 290))
    main.win.blit(main.ship5Exhaust, (435, 320))

    main.win.blit(main.ship6Skin, (660, 290))
    main.win.blit(main.ship6Exhaust, (635, 315))

def formatText(title):
    ship = next((skin for skin in main.skins if skin.title == title), None)

    if ship == None:
        return '1000$'
    else:
        if main.selectedSkin.title == title:
            return 'equipped'
        
        return 'avaiable'

def formatColor(title):
    ship = next((skin for skin in main.skins if skin.title == title), None)
    color = (50, 168, 82)

    if main.money < 1000:
        color = (145, 33, 23)


    if ship == None:
        return color
    else:
        return (255, 255, 255)

def equipSkin(skin):
    if not skin.equipped:
        for s in main.skins:
            s.equipped = False
        skin.equipped = True
        main.selectedSkin = skin
        main.SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load(main.selectedSkin.image), (84, 84))
        main.SPACESHIP_EXHAUST_IMAGE = pygame.transform.scale(pygame.image.load(main.selectedSkin.exhaust), (32, 32))
        main.PROJECTILE_IMAGE = pygame.transform.scale(pygame.image.load(main.selectedSkin.projectile), (32, 32))