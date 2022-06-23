import pygame
import os.path
from button import Button
from textWithOutline import Text
import json
from skin import Skin
from slider import SLIDER
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
    Skin('Ship 1', 'Assets/Ship1/Ship1.png', 'Assets/Ship1/Exhaust/Normal_flight/Exhaust1/exhaust4.png', 'Assets/Shots/Shot1/shot1_asset.png', True)
]
selectedSkin = None

for skin in skins:
    if skin.equipped:
        selectedSkin = skin
        break


def generateFile():
    skinArr = []

    for skin in skins:
        skinArr.append({'title': skin.title, 'equipped': skin.equipped})

    data = {
        "shipSpeed": shipSpeed,
        "shipDmg": shipDmg,
        "attackSpeed": attackSpeed,
        "shipHealth": shipHealth,
        "money": money,
        "stage": stage,
        "skins": skinArr
    }

    with open('data_save.txt', 'w') as data_save_file:
        json.dump(data, data_save_file)

def generateSaveOptionsFile():
    optionsData = {
        "musicVolume": musicSlider.value,
        "soundVolume": soundSlider.value
    }
    with open('optionsData.txt', 'w') as data_save_file:
        json.dump(optionsData, data_save_file)

        
#MENU
startBtnWidth, startBtnHeight = WIDTH/6, HEIGHT/8
playButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/Start_Button.png'),(startBtnWidth,startBtnHeight))
loadButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/LoadButton.png'),(startBtnWidth,startBtnHeight))
exitButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/ExitButton.png'),(startBtnWidth,startBtnHeight))
optionsButtonImg = pygame.transform.scale(pygame.image.load('Assets/Buttons/OptionsButton.png'),(startBtnWidth,startBtnHeight))
PLAY_BUTTON = Button(WIDTH/2,startBtnHeight+30,playButtonImg)
LOAD_BUTTON = Button(WIDTH/2,(startBtnHeight+30)*2,loadButtonImg)
OPTIONS_BUTTON = Button(WIDTH/2,(startBtnHeight+30)*3,optionsButtonImg)
EXIT_BUTTON = Button(WIDTH/2,(startBtnHeight+30)*4,exitButtonImg)


#OPTIONS
musicVolume = 0.5
soundVolume = 1
if os.path.exists('optionsData.txt'):
    with open('optionsData.txt') as data_save_file:
        optionsData = json.load(data_save_file)
        musicVolume = optionsData['musicVolume']
        soundVolume = optionsData['soundVolume']

musicSlider = SLIDER(win, "Music", WIDTH // 2, HEIGHT // 2 + 100, 300, musicVolume)
soundSlider = SLIDER(win, "Sounds", WIDTH // 2, HEIGHT // 2 - 100, 300, soundVolume)


#GAME
SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load(selectedSkin.image), (84, 84))
SPACESHIP_EXHAUST_IMAGE = pygame.transform.scale(pygame.image.load(selectedSkin.exhaust), (32, 32))
PROJECTILE_IMAGE = pygame.transform.scale(pygame.image.load(selectedSkin.projectile), (32, 32))
METEOR_IMAGE = pygame.transform.scale(pygame.image.load('Assets/Meteor/meteor_big.png'), (84, 68))
enemyImg = pygame.transform.scale(pygame.image.load('Assets/Enemies/vehicle 1/frames/vehicle-1.png'), (126, 66))
ENEMY_IMAGE = pygame.transform.flip(enemyImg, True, False)
enemyProjectileImg = pygame.transform.scale(pygame.image.load('Assets/Enemies/bullet_red.png'), (32, 32))
ENEMY_PROJECTILE_IMAGE = pygame.transform.flip(enemyProjectileImg, True, False)
bossProjectileImg = pygame.transform.scale(pygame.image.load('Assets/bossSprites/bullet.png'), (512, 512))
BOSS_PROJECTILE_IMAGE = pygame.transform.flip(bossProjectileImg, True, False)
bullets = []
enemyBullets = []
meteors = []
moneyTexts = []
explosions = []
enemyIndexes = []
bulletIndexes = []
enemyBulletsIndexes = []
bossBullets = []
bossBulletsIndexes = []
meteorIndexes = []
enemies = []
moneyTextIndexes = []
explosionIndexes = []
gameOverText = Text(WIDTH//2,HEIGHT//2,"GAME OVER",60,(255,255,255),False)
pauseText = Text(WIDTH//2,HEIGHT//2,"PAUSE",60,(255,255,255),False)
levelCompletedText = Text(WIDTH//2,HEIGHT//2,"LEVEL COMPLETED!",60,(255,255,255),False)
stageText = Text(WIDTH // 2, HEIGHT // 4, f"LEVEL {stage}", 50, (255, 255, 255), False)
thanks4playingText = Text(WIDTH // 2, HEIGHT // 4, f"THANKS FOR PLAYING", 50, (255, 255, 255), False)
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
gameWon = False

#SOUNDS

shootingSound = pygame.mixer.Sound('Assets/sounds/shooting.wav')
shootingSound.set_volume(soundVolume)
asteroidExplosionSound = pygame.mixer.Sound('Assets/sounds/asteroidexplosin.wav')
asteroidExplosionSound.set_volume(soundVolume)
shipExplosionSound = pygame.mixer.Sound('Assets/sounds/shipexplosion.wav')
shipExplosionSound.set_volume(soundVolume)

bgMusic = pygame.mixer.music.load('Assets/sounds/backgroundMusic.mp3')
pygame.mixer.music.set_volume(musicVolume)


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

ship1SkinImage = 'Assets/Ship1/Ship1.png'
ship1ExhaustImage = 'Assets/Ship1/Exhaust/Normal_flight/Exhaust1/exhaust4.png'
ship1ProjectileImage = 'Assets/Shots/Shot1/shot1_asset.png'
ship1Skin = pygame.transform.scale(pygame.image.load(ship1SkinImage),(84,84))
ship1Exhaust = pygame.transform.scale(pygame.image.load(ship1ExhaustImage), (32, 32))

ship2SkinImage = 'Assets/Ship2/Ship2.png'
ship2ExhaustImage = 'Assets/Ship2/Exhaust/Normal_flight/Exhaust1/exhaust4.png'
ship2ProjectileImage = 'Assets/Shots/Shot2/shot2_asset.png'
ship2Skin = pygame.transform.scale(pygame.image.load(ship2SkinImage),(84,84))
ship2Exhaust = pygame.transform.scale(pygame.image.load(ship2ExhaustImage), (32, 32))

ship3SkinImage = 'Assets/Ship3/Ship3.png'
ship3ExhaustImage = 'Assets/Ship3/Exhaust/Normal_flight/Exhaust1/exhaust4.png'
ship3ProjectileImage = 'Assets/Shots/Shot3/shot3_asset.png'
ship3Skin = pygame.transform.scale(pygame.image.load(ship3SkinImage),(84,84))
ship3Exhaust = pygame.transform.scale(pygame.image.load(ship3ExhaustImage), (32, 32))

ship4SkinImage = 'Assets/Ship4/Ship4.png'
ship4ExhaustImage = 'Assets/Ship4/Exhaust/Normal_flight/Exhaust1/exhaust4.png'
ship4ProjectileImage = 'Assets/Shots/Shot4/shot4_asset.png'
ship4Skin = pygame.transform.scale(pygame.image.load(ship4SkinImage),(84,84))
ship4Exhaust = pygame.transform.scale(pygame.image.load(ship4ExhaustImage), (32, 32))

ship5SkinImage = 'Assets/Ship5/Ship5.png'
ship5ExhaustImage = 'Assets/Ship5/Exhaust/Normal_flight/Exhaust1/exhaust4.png'
ship5ProjectileImage = 'Assets/Shots/Shot5/shot5_asset.png'
ship5Skin = pygame.transform.scale(pygame.image.load(ship5SkinImage),(84,84))
ship5Exhaust = pygame.transform.scale(pygame.image.load(ship5ExhaustImage), (32, 32))

ship6SkinImage = 'Assets/Ship6/Ship6.png'
ship6ExhaustImage = 'Assets/Ship6/Exhaust/Normal_flight/Exhaust1/exhaust4.png'
ship6ProjectileImage = 'Assets/Shots/Shot6/shot6_asset.png'
ship6Skin = pygame.transform.scale(pygame.image.load(ship6SkinImage),(84,84))
ship6Exhaust = pygame.transform.scale(pygame.image.load(ship6ExhaustImage), (32, 32))

imageBg = pygame.transform.scale(pygame.image.load('Assets/SpaceBG.png'),(WIDTH,HEIGHT))
run = True
runMenu = True
runGame = False

import mainMenu

if __name__=="__main__":
    pygame.mixer.music.play(-1)
    mainMenu.menu()
    pygame.quit()
