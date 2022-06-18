import pygame
from button import Button
from textWithOutline import Text
import json
from skin import Skin
pygame.init()

FPS = 60
clock = pygame.time.Clock()

WIDTH = 1920 // 2
HEIGHT = 1080 // 2

win = pygame.display.set_mode((WIDTH, HEIGHT))
fillColor = (0, 0, 0)
win.fill(fillColor)
pygame.display.flip()

shipSpeed = 0
shipDmg = 0
attackSpeed = 0
shipHealth = 0
money = 0
stage = 1
skins = [
    Skin('Ship 1', 'Assets/Ship1/Ship1.png', 'Assets/Ship1/Exhaust/Normal_flight/Exhaust1/exhaust4.png', True)
]
selectedSkin = None

for skin in skins:
    if skin.equipped:
        selectedSkin = skin
        break


def generateFile():
    data = {
        "shipSpeed": shipSpeed,
        "shipDmg": shipDmg,
        "attackSpeed": attackSpeed,
        "shipHealth": shipHealth,
        "money": money,
        "stage": stage
    }

    with open('data_save.txt', 'w') as data_save_file:
        json.dump(data, data_save_file)

#MENU
startBtnWidth, startBtnHeight = WIDTH/6, HEIGHT/8
playButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/Start_Button.png'),(startBtnWidth,startBtnHeight))
loadButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/LoadButton.png'),(startBtnWidth,startBtnHeight))
exitButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/ExitButton.png'),(startBtnWidth,startBtnHeight))
PLAY_BUTTON = Button(WIDTH/2,startBtnHeight+30,playButtonImg)
LOAD_BUTTON = Button(WIDTH/2,(startBtnHeight+30)*2,loadButtonImg)
EXIT_BUTTON = Button(WIDTH/2,(startBtnHeight+30)*3,exitButtonImg)


#GAME
SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load(selectedSkin.image), (84, 84))
SPACESHIP_EXHAUST_IMAGE = pygame.transform.scale(pygame.image.load(selectedSkin.exhaust), (32, 32))
PROJECTILE_IMAGE = pygame.transform.scale(pygame.image.load('Assets/Shots/Shot1/shot1_asset.png'), (32, 32))
METEOR_IMAGE = pygame.transform.scale(pygame.image.load('Assets/Meteor/meteor_big.png'), (84, 68))
bullets = []
meteors = []
moneyTexts = []
explosions = []
bulletIndexes = []
meteorIndexes = []
moneyTextIndexes = []
explosionIndexes = []
gameOverText = Text(WIDTH//2,HEIGHT//2,"GAME OVER",60,(255,255,255),False)
pauseText = Text(WIDTH//2,HEIGHT//2,"PAUSE",60,(255,255,255),False)
levelCompletedText = Text(WIDTH//2,HEIGHT//2,"LEVEL COMPLETED!",60,(255,255,255),False)
stageText = Text(WIDTH // 2, HEIGHT // 4, f"LEVEL {stage}", 50, (255, 255, 255), False)
timerText = Text(WIDTH // 2, HEIGHT // 4, f"03:00", 50, (255, 255, 255), False)

hp0 = pygame.transform.scale(pygame.image.load('Assets/health/heart0.png'), (17*3, 17*3))
hp3 = pygame.transform.scale(pygame.image.load('Assets/health/heart3.png'), (17*3, 17*3))

shopButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/Shop_Button.png'),(startBtnWidth,startBtnHeight))
nextButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/NextButton.png'),(startBtnWidth,startBtnHeight))
resetButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/ResetButton.png'),(startBtnWidth,startBtnHeight))
exitToMenuButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/ExitButton.png'),(startBtnWidth,startBtnHeight))
SHOP_BUTTON = Button(startBtnWidth,HEIGHT-startBtnHeight,shopButtonImg)
NEXT_BUTTON = Button(WIDTH - startBtnWidth,HEIGHT-startBtnHeight,nextButtonImg)
RESET_BUTTON = Button(WIDTH - startBtnWidth,HEIGHT-startBtnHeight,resetButtonImg)
EXIT_TO_MENU_BUTTON = Button(WIDTH // 2, HEIGHT - startBtnHeight, exitToMenuButtonImg)

shootingSound = pygame.mixer.Sound('Assets/sounds/shooting.wav')
asteroidExplosionSound = pygame.mixer.Sound('Assets/sounds/asteroidexplosin.wav')
shipExplosionSound = pygame.mixer.Sound('Assets/sounds/shipexplosion.wav')

bgMusic = pygame.mixer.music.load('Assets/sounds/backgroundMusic.wav')

#SHOP
shopBg = pygame.transform.scale(pygame.image.load('Assets/shopBG.png'),(WIDTH,HEIGHT))
shopText = Text(WIDTH // 2, 50,"shop",100,(255,255,255),True)
skinButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/skinsButton.png'),(startBtnWidth,startBtnHeight))
SKIN_BUTTON = Button(WIDTH - 100, HEIGHT - 50,skinButtonImg)

#SKIN SHOP
skinShopText = Text(WIDTH // 2, 50,"skins",100,(255,255,255),True)
ship1Item = pygame.Rect(220, 150, 150, 100)
ship2Item = pygame.Rect(420, 150, 150, 100)
ship3Item = pygame.Rect(620, 150, 150, 100)
ship4Item = pygame.Rect(220, 290, 150, 100)
ship5Item = pygame.Rect(420, 290, 150, 100)
ship6Item = pygame.Rect(620, 290, 150, 100)
BACK_SHOP_BUTTON = Button(100, HEIGHT - 50, shopButtonImg)

ship1Skin = pygame.transform.scale(pygame.image.load('Assets/Ship1/Ship1.png'),(84,84))
ship1Exhaust = pygame.transform.scale(pygame.image.load('Assets/Ship1/Exhaust/Normal_flight/Exhaust1/exhaust4.png'), (32, 32))

ship2Skin = pygame.transform.scale(pygame.image.load('Assets/Ship2/Ship2.png'),(84,84))
ship2Exhaust = pygame.transform.scale(pygame.image.load('Assets/Ship2/Exhaust/Normal_flight/Exhaust1/exhaust4.png'), (32, 32))

ship3Skin = pygame.transform.scale(pygame.image.load('Assets/Ship3/Ship3.png'),(84,84))
ship3Exhaust = pygame.transform.scale(pygame.image.load('Assets/Ship3/Exhaust/Normal_flight/Exhaust1/exhaust4.png'), (32, 32))

ship4Skin = pygame.transform.scale(pygame.image.load('Assets/Ship4/Ship4.png'),(84,84))
ship4Exhaust = pygame.transform.scale(pygame.image.load('Assets/Ship4/Exhaust/Normal_flight/Exhaust1/exhaust4.png'), (32, 32))

ship5Skin = pygame.transform.scale(pygame.image.load('Assets/Ship5/Ship5.png'),(84,84))
ship5Exhaust = pygame.transform.scale(pygame.image.load('Assets/Ship5/Exhaust/Normal_flight/Exhaust1/exhaust4.png'), (32, 32))

ship6Skin = pygame.transform.scale(pygame.image.load('Assets/Ship6/Ship6.png'),(84,84))
ship6Exhaust = pygame.transform.scale(pygame.image.load('Assets/Ship6/Exhaust/Normal_flight/Exhaust1/exhaust4.png'), (32, 32))

imageBg = pygame.transform.scale(pygame.image.load('Assets/SpaceBG.png'),(WIDTH,HEIGHT))
run = True
runMenu = True
runGame = False

import mainMenu

if __name__=="__main__":
    pygame.mixer.music.play(-1)
    mainMenu.menu()
    # skinShop.shop()
    pygame.quit()
