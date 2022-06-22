import pygame
import threading
import main
from meteor import Meteor
from random import randint
from spaceship import Spaceship, Projectile
from fade import fadeOut
from shop import shop
from textWithOutline import Text
from particles import moneyEarned,asteroidExplosion,projectileExplosion
from enemy import Enemy
from bossClass import BOSS

x = 50
y = main.HEIGHT / 2
SPACESHIP = Spaceship(x, y)
SPACESHIP.rect.x = x
SPACESHIP.rect.y = y
t = None

def gameOver():
    t.cancel()
    enemyT.cancel()
    main.runGame = False
    greyOverlay = pygame.Surface((main.WIDTH,main.HEIGHT))
    greyOverlay = greyOverlay.convert()
    greyOverlay.fill((100,100,100))
    greyOverlay.set_alpha(150)
    main.win.blit(greyOverlay,(0,0))
    main.gameOverText.draw(main.win)
    main.meteors = []
    main.bullets = []
    main.enemies = []
    main.explosions = []
    main.moneyTexts = []
    main.SHOP_BUTTON.draw(main.win)
    main.RESET_BUTTON.draw(main.win)
    main.EXIT_TO_MENU_BUTTON.draw(main.win)
    pygame.display.update()
    while main.run and not main.runGame:
        if main.SHOP_BUTTON.check():
            fadeOut()
            shop()
        elif main.EXIT_TO_MENU_BUTTON.check():
            fadeOut()
            main.runMenu = True
            main.runGame = False
            main.generateFile()
            main.mainMenu.menu()
        elif main.RESET_BUTTON.check():
            fadeOut()
            if main.stage == 10:
                bossBattle()
            else:
                game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.run = False
    if main.runGame:
        if main.stage == 10:
            bossBattle()
        else:
            game()

def pause():
    t.cancel()
    enemyT.cancel()
    main.runGame = False
    greyOverlay = pygame.Surface((main.WIDTH,main.HEIGHT))
    greyOverlay = greyOverlay.convert()
    greyOverlay.fill((100,100,100))
    greyOverlay.set_alpha(150)
    main.win.blit(greyOverlay,(0,0))
    main.pauseText.draw(main.win)
    main.EXIT_TO_MENU_BUTTON.draw(main.win)
    pygame.display.update()
    while main.run and not main.runGame:
        if main.EXIT_TO_MENU_BUTTON.check():
            fadeOut()
            main.runMenu = True
            main.runGame = False
            main.generateFile()
            main.mainMenu.menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main.runGame = True
    if main.runGame:
        meteorsGen()

def startGame():
    main.meteors = []
    main.bullets = []
    main.enemies = []
    main.explosions = []
    main.moneyTexts = []
    main.stageText = Text(main.WIDTH//2,main.HEIGHT//2,f"LEVEL {main.stage}",50,(255,255,255),False)
    main.timerText = Text(main.WIDTH - 100, 50, f"03:00", 50, (255, 255, 255), False)
    SPACESHIP.image = main.SPACESHIP_IMAGE
    SPACESHIP.exhaust_image = main.SPACESHIP_EXHAUST_IMAGE
    SPACESHIP.resetPos(main.win)

def finishGame():
    t.cancel()
    enemyT.cancel()
    main.stage += 1
    main.runGame = False
    greyOverlay = pygame.Surface((main.WIDTH, main.HEIGHT))
    greyOverlay = greyOverlay.convert()
    greyOverlay.fill((100, 100, 100))
    greyOverlay.set_alpha(150)
    main.win.blit(greyOverlay, (0, 0))
    main.levelCompletedText.draw(main.win)
    main.meteors = []
    main.bullets = []
    main.enemies = []
    main.explosions = []
    main.moneyTexts = []
    main.SHOP_BUTTON.draw(main.win)
    main.EXIT_TO_MENU_BUTTON.draw(main.win)
    main.NEXT_BUTTON.draw(main.win)
    pygame.display.update()
    while main.run and not main.runGame:
        if main.SHOP_BUTTON.check():
            fadeOut()
            shop()
        elif main.EXIT_TO_MENU_BUTTON.check():
            fadeOut()
            main.runMenu = True
            main.runGame = False
            main.generateFile()
            main.mainMenu.menu()
        elif main.RESET_BUTTON.check():
            fadeOut()
            if main.stage == 10:
                bossBattle()
            else:
                game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.run = False
    if main.runGame:
        if main.stage == 10:
            bossBattle()
        else:
            game()

def game():
    br = 0
    minutes = 3
    seconds = 0
    if main.run:
        startGame()
        health = main.shipHealth
        meteorsGen()
        enemiesSpawn()
        space_pressed = False
        previous_time = pygame.time.get_ticks() - 1000
        previous_time_hit = pygame.time.get_ticks() - 1000

    while main.run and not main.runMenu:
        main.clock.tick(main.FPS)
        main.win.blit(main.imageBg, (0, 0))
        main.timerText.draw(main.win)
        drawHealth(health)
        SPACESHIP.draw(main.win)

        if br % 60 == 0 and br != 0:
            if seconds - 1 < 0:
                minutes -= 1
                seconds = 59
            else:
                seconds -= 1

            main.timerText = Text(main.WIDTH - 100, 50, f"0{minutes}:{seconds if seconds > 9 else f'0{seconds}'}", 50, (255, 255, 255), False)

        if minutes == 0 and seconds == 5:
            t.cancel()

        if minutes == 0 and seconds == 0:
            finishGame()


        for bullet in main.bullets:
            if bullet.x < main.WIDTH and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                main.bulletIndexes.append(main.bullets.index(bullet))
        
        for enemy in main.enemies:
            enemy.draw(main.win)
            if enemy.x < main.WIDTH and enemy.x > 0 - 126:
                enemy.x -= enemy.vel
            else:
                main.enemyIndexes.append(main.enemies.index(enemy))
            
            for bullet in main.bullets:
                if bullet.hitbox.colliderect(enemy.hitbox):
                    if enemy.takeDmg():
                        main.asteroidExplosionSound.stop()
                        main.asteroidExplosionSound.play()
                        main.money += enemy.multiplier
                        main.moneyTexts.append(moneyEarned(enemy.multiplier, 30, enemy.x, enemy.y))
                        main.enemyIndexes.append(main.enemies.index(enemy))
                        main.explosions.append(asteroidExplosion(10, enemy.hitbox.x + enemy.width // 2, enemy.hitbox.y + enemy.height // 2, 3))
                        
                    main.bulletIndexes.append(main.bullets.index(bullet))
                    main.explosions.append(projectileExplosion(10,bullet.x ,bullet.y,1,main.selectedSkin.title[5]))

        for meteor in main.meteors:
            meteor.draw(main.win)
            if meteor.x < main.WIDTH and meteor.x > 0 - 84:
                meteor.x -= meteor.vel
            else:
                main.meteorIndexes.append(main.meteors.index(meteor))

            for bullet in main.bullets:
                if bullet.hitbox.colliderect(meteor.hitbox):
                    if meteor.takeDmg():
                        main.asteroidExplosionSound.stop()
                        main.asteroidExplosionSound.play()
                        main.money+=meteor.multiplier
                        main.moneyTexts.append(moneyEarned(meteor.multiplier,30,meteor.x,meteor.y))
                        main.meteorIndexes.append(main.meteors.index(meteor))
                        main.explosions.append(asteroidExplosion(10, meteor.hitbox.x + meteor.width // 2, meteor.hitbox.y + meteor.height // 2, 3))
                    main.bulletIndexes.append(main.bullets.index(bullet))
                    main.explosions.append(projectileExplosion(10,bullet.x ,bullet.y,1,main.selectedSkin.title[5]))

            if SPACESHIP.hitbox.colliderect(meteor.hitbox):
                current_time_hit = pygame.time.get_ticks()
                if current_time_hit - previous_time_hit > 1000:
                    previous_time_hit = current_time_hit
                    health -= 1
                    if health == 0:
                        main.shipExplosionSound.play()
                        gameOver()

        for moneyText in main.moneyTexts:
            if moneyText.draw(main.win):
                main.moneyTextIndexes.append(main.moneyTexts.index(moneyText))

        for Explosion in main.explosions:
            if Explosion.draw(main.win):
                main.explosionIndexes.append(main.explosions.index(Explosion))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                SPACESHIP.movement(event.key)
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                elif event.key == pygame.K_ESCAPE:
                    pause()
            elif event.type == pygame.KEYUP:
                SPACESHIP.stop(event.key)
                if event.key == pygame.K_SPACE:
                    space_pressed = False

            if event.type == pygame.QUIT:
                main.run = False

        if space_pressed:
            current_time = pygame.time.get_ticks()
            if current_time - previous_time > 1000/main.attackSpeed:
                previous_time = current_time
                main.shootingSound.stop()
                main.shootingSound.play()
                main.bullets.append(Projectile(round(SPACESHIP.rect.x + SPACESHIP.width // 2 + 10),round(SPACESHIP.rect.y + 28), main.win))
        SPACESHIP.update(main.bullets)

        try:
            for i in range(len(main.meteorIndexes)):
                main.meteors.pop(main.meteorIndexes[i]-i)
            main.meteorIndexes = []
        except:
            print("meteor")
            main.meteorIndexes = []
        try:
            for i in range(len(main.enemyIndexes)):
                main.enemies.pop(main.enemyIndexes[i]-i)
            main.enemyIndexes = []
        except:
            print("enemy")
            main.enemyIndexes = []
        try:
            for i in range(len(main.bulletIndexes)):
                main.bullets.pop(main.bulletIndexes[i]-i)
            main.bulletIndexes = []
        except:
            print("bullet")
            main.bulletIndexes = []
        try:
            for i in range(len(main.moneyTextIndexes)):
                main.moneyTexts.pop(main.moneyTextIndexes[i]-i)
            main.moneyTextIndexes = []
        except:
            print("money")
            main.moneyTextIndexes = []
        try:
            for i in range(len(main.explosionIndexes)):
                main.explosions.pop(main.explosionIndexes[i]-i)
            main.explosionIndexes = []
        except:
            print("explosion")
            main.explosionIndexes = []

        br+=1
        pygame.display.update()
    if main.runMenu == True:
        fadeOut()
    t.cancel()

def bossBattle():
    if main.run:
        startGame()
        health = main.shipHealth
        boss = BOSS(main.WIDTH,main.HEIGHT//2,330,160)
        space_pressed = False
        previous_time = pygame.time.get_ticks() - 1000
        previous_time_hit = pygame.time.get_ticks() - 1000
        boss.bringBoss()

    while main.run and not main.runMenu:
        main.clock.tick(main.FPS)
        main.win.blit(main.imageBg, (0, 0))
        drawHealth(health)
        SPACESHIP.draw(main.win)

        for bullet in main.bullets:
            if bullet.x < main.WIDTH and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                main.bulletIndexes.append(main.bullets.index(bullet))

            #for bullet in main.bullets:

        #spaceship getting hit
        if SPACESHIP.hitbox.colliderect(boss.hitbox1):
            current_time_hit = pygame.time.get_ticks()
            if current_time_hit - previous_time_hit > 1000:
                previous_time_hit = current_time_hit
                health -= 1
                if health == 0:
                    main.shipExplosionSound.play()
                    gameOver()
        #draw explosions
        for Explosion in main.explosions:
            if Explosion.draw(main.win):
                main.explosionIndexes.append(main.explosions.index(Explosion))
        #check for movement
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                SPACESHIP.movement(event.key)
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                elif event.key == pygame.K_ESCAPE:
                    pause()
            elif event.type == pygame.KEYUP:
                SPACESHIP.stop(event.key)
                if event.key == pygame.K_SPACE:
                    space_pressed = False

            if event.type == pygame.QUIT:
                main.run = False
        #fire a shot
        if space_pressed:
            current_time = pygame.time.get_ticks()
            if current_time - previous_time > 1000/main.attackSpeed:
                previous_time = current_time
                main.shootingSound.stop()
                main.shootingSound.play()
                main.bullets.append(Projectile(round(SPACESHIP.rect.x + SPACESHIP.width // 2 + 10),round(SPACESHIP.rect.y + 28), main.win))
        SPACESHIP.update(main.bullets)
        #delete bullets and explosions
        try:
            for i in range(len(main.bulletIndexes)):
                main.bullets.pop(main.bulletIndexes[i]-i)
            main.bulletIndexes = []
        except:
            print("bullet")
            main.bulletIndexes = []
        try:
            for i in range(len(main.explosionIndexes)):
                main.explosions.pop(main.explosionIndexes[i]-i)
            main.explosionIndexes = []
        except:
            print("explosion")
            main.explosionIndexes = []

        boss.draw(main.win)
        boss.update()

        pygame.display.update()
    if main.runMenu == True:
        fadeOut()
    t.cancel()



def drawHealth(health):

    for i in range(5):
        if health-3*i>3:
            main.win.blit(main.hp3, (17 * 3 * i + i*3, 0))
        elif health-3*i<=0:
            main.win.blit(main.hp0, (17 * 3 * i + i*3, 0))
        else:
            main.win.blit(pygame.transform.scale(pygame.image.load(f'Assets/health/heart{health-3*i}.png'), (17*3, 17*3)), (17 * 3 * i + i*3, 0))

def meteorsGen():
    global t
    METEOR = Meteor(main.WIDTH-10, randint(-34, main.HEIGHT - 68),randint(2*main.stage,4*main.stage))
    main.meteors.append(METEOR)
    t = threading.Timer(1-main.stage/20, meteorsGen)
    t.start()

def enemiesSpawn():
    global enemyT
    if len(main.enemies) < 5:
        enemy = Enemy(main.WIDTH-126, randint(66, main.HEIGHT - 66), randint(2*main.stage,4*main.stage))
        main.enemies.append(enemy)
    enemyT = threading.Timer(1-main.stage/20, enemiesSpawn)
    enemyT.start()
