import pygame
import main
from upgradeBar import upgrade
from fade import fadeOut
from textWithOutline import Text

offCenterX = 150
offCenterY = 70


def shop():
    if main.run:
        print(main.shipSpeed)
        speedUpgrade = upgrade(main.shipSpeed, main.WIDTH // 2 - offCenterX, main.HEIGHT // 2 - offCenterY, "Speed")
        dmgUpgrade = upgrade(main.shipDmg, main.WIDTH // 2 + offCenterX, main.HEIGHT // 2 - offCenterY, "Damage")
        healthUpgrade = upgrade(main.shipHealth, main.WIDTH // 2 - offCenterX, main.HEIGHT // 2 + offCenterY, "Health")
        attackSpeedUpgrade = upgrade(main.attackSpeed, main.WIDTH // 2 + offCenterX, main.HEIGHT // 2 + offCenterY, "Attack speed")
        drawShop(speedUpgrade,dmgUpgrade,healthUpgrade,attackSpeedUpgrade)
    while main.run and not main.runGame:
        main.clock.tick(main.FPS)

        updateShop(speedUpgrade,dmgUpgrade,healthUpgrade,attackSpeedUpgrade)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main.runGame = True
                    fadeOut()

def drawShop(speedUpgrade,dmgUpgrade,healthUpgrade,attackSpeedUpgrade):
    main.win.blit(main.shopBg, (0, 0))
    main.shopText.draw(main.win)
    moneyText = Text(100, 50, f"{main.money}$", 20, (46, 120, 40), True)
    moneyText.draw(main.win)

    speedUpgrade.draw(main.win)
    dmgUpgrade.draw(main.win)
    healthUpgrade.draw(main.win)
    attackSpeedUpgrade.draw(main.win)

    pygame.display.update()

def updateShop(speedUpgrade,dmgUpgrade,healthUpgrade,attackSpeedUpgrade):
    if speedUpgrade.check():
        main.shipSpeed = speedUpgrade.buy()
        drawShop(speedUpgrade,dmgUpgrade,healthUpgrade,attackSpeedUpgrade)

    if dmgUpgrade.check():
        main.shipDmg = dmgUpgrade.buy()
        drawShop(speedUpgrade,dmgUpgrade,healthUpgrade,attackSpeedUpgrade)

    if healthUpgrade.check():
        main.shipHealth = healthUpgrade.buy()
        drawShop(speedUpgrade,dmgUpgrade,healthUpgrade,attackSpeedUpgrade)

    if attackSpeedUpgrade.check():
        main.attackSpeed = attackSpeedUpgrade.buy()
        drawShop(speedUpgrade,dmgUpgrade,healthUpgrade,attackSpeedUpgrade)

    pygame.display.update()