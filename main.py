import pygame, sys, time, math, random
import pygame.image as im2g

import pygame.font as pyfont

from buttonClass import button, settingsButton
from droneClass import drone
from fireClass import Fire

pygame.init()
windowSize = [1280,768]
window = pygame.display.set_mode(windowSize)

igFont = pyfont.SysFont(name="Gabriola",size=48)

## images
# main menu images
mainMenuImg = im2g.load("./assets/menu/mainMenu.png")
mm_titleImg = im2g.load("./assets/menu/title.png")

mm_startGameImg = im2g.load("./assets/menu/start_game.png")
mm_startGameImg_sel = im2g.load("./assets/menu/start_game_sel.png")

mm_settingsImg = im2g.load("./assets/menu/settings.png")
mm_settingsImg_sel = im2g.load("./assets/menu/settings_sel.png")

mm_exitImg = im2g.load("./assets/menu/exit.png")
mm_exitImg_sel = im2g.load('./assets/menu/exit_sel.png')

# settings menu images
settingsMenuImg = im2g.load("./assets/settings/settings_menu.png")

se_settingsExitImg = im2g.load("./assets/settings/return.png")
se_settingsExitImg_sel = im2g.load("./assets/settings/return_sel.png")

se_AI_notSelected_F = im2g.load('./assets/settings/ai_ns_f.png')
se_AI_notSelected_T = im2g.load("./assets/settings/ai_ns_t.png")

se_AI_selected_F = im2g.load('./assets/settings/ai_s_f.png')
se_AI_selected_T = im2g.load("./assets/settings/ai_s_t.png")

# pre-game menu images
pre_gameMenuImg = im2g.load("./assets/pre_game/lore.png")

pgExitImg = im2g.load("./assets/pre_game/return.png")
pgExitImg_sel = im2g.load("./assets/pre_game/return_sel.png")

pgEasyImg = im2g.load("./assets/pre_game/easy.png")
pgEasyImg_sel = im2g.load("./assets/pre_game/easy_sel.png")

pgMediumImg = im2g.load("./assets/pre_game/medium.png")
pgMediumImg_sel = im2g.load("./assets/pre_game/medium_sel.png")

pgHardImg = im2g.load("./assets/pre_game/hard.png")
pgHardImg_sel = im2g.load("./assets/pre_game/hard_sel.png")

# drone images

gDrone1 = im2g.load("./assets/game/drone.png")

# in-game images
ig_background = im2g.load("./assets/game/background.png")
ig_background_w = im2g.load("./assets/game/background_win.png")
ig_background_l = im2g.load("./assets/game/background_lose.png")

fire_img1 = im2g.load("./assets/game/fire.png")
fire_img2 = im2g.load("./assets/game/fire2.png") 

ig_waterDisp = im2g.load("./assets/game/water_container.png")

ig_waterDisplay = im2g.load("./assets/game/water_reservoir.png")

# lose screen button

lc_return = im2g.load("./assets/lose_screen/return.png")
lc_return_sel = im2g.load("./assets/lose_screen/return_sel.png")

# win screen button

wc_return = im2g.load("./assets/win_screen/return.png")
wc_return_sel = im2g.load("./assets/win_screen/return_sel.png")



## game vars

#ingame ticks
fireTick = 0
fires = []

buttonsDown = []
gameState = 0 
# 0 - main menu, 1 - start game menu, 2 - settings, 3 - about, 4 - game, 5 - shop?, 6 - win screen, 7 - lose screen
def setState(num):
	global gameState
	gameState = num

def setDifficultyAndStartGame(diff):
	global gameSettings,gameState,fires,currentGameStats
	gameState = 4
	gameSettings["difficulty"] = diff
	player.x = windowSize[0]/2
	player.y = windowSize[1]-gDrone1.get_size()[1]
	player.water = 100
	while len(fires) < 5:
		fires.append(createFire())

	if(gameSettings["difficulty"] == 0):
		gameSettings["fireSpreadSpeed"] = 100
		gameSettings["usingWater"] = False
		gameSettings["loseOnXFires"] = 50
	elif(gameSettings["difficulty"] == 1):
		gameSettings["fireSpreadSpeed"] = 75
		gameSettings["usingWater"] = True
		gameSettings["loseOnXFires"] = 25
	elif(gameSettings["difficulty"] == 2):
		gameSettings["fireSpreadSpeed"] = 50
		gameSettings["usingWater"] = True
		gameSettings["loseOnXFires"] = 10

	currentGameStats = {
		"waterSpent": 0,
		"firesPutOut": 0,
	}

paused = False

settings = {
	"musicVolume": 0,
	"useAI": False
}

gameSettings = {
	"difficulty": 0,
	"usingWater": False,
	"fireSpreadSpeed": 120,
	"loseOnXFires": 200,
}

playerStats = {
	"water": 100,
	"droneSpeed": 15
}

currentGameStats = {
	"waterSpent": 0,
	"firesPutOut": 0,
}

## buttons
# main menu buttons
mmButtons = []
mmButtons.append(button(0, 400, mm_startGameImg, mm_startGameImg_sel, lambda: setState(1)))
mmButtons.append(button(0, 475, mm_settingsImg, mm_settingsImg_sel, lambda: setState(2)))
mmButtons.append(button(0, 685, mm_exitImg, mm_exitImg_sel, lambda: sys.exit()))

# settings menu buttons
seButtons = []
seButtons.append(button(420,380, se_settingsExitImg, se_settingsExitImg_sel, lambda: setState(0)))
seButtons.append(settingsButton(402,83, se_AI_notSelected_F, se_a))

# pregame menu buttons
pgButtons = []
pgButtons.append(button(7, 551, pgEasyImg, pgEasyImg_sel, lambda: setDifficultyAndStartGame(0)))
pgButtons.append(button(451, 556, pgMediumImg, pgMediumImg_sel, lambda: setDifficultyAndStartGame(1)))
pgButtons.append(button(906, 560, pgHardImg, pgHardImg_sel, lambda: setDifficultyAndStartGame(2)))
pgButtons.append(button(558, 708, pgExitImg, pgExitImg_sel, lambda: setState(0)))

# lose menu button

returnFromLoseButton = button(377,670, lc_return, lc_return_sel, lambda: setState(0))

# win return button
returnFromWinButton = button(377,670, wc_return, wc_return_sel, lambda: setState(0))

## player
# drone
player = drone(windowSize[0]/2,windowSize[1]-gDrone1.get_size()[1],[gDrone1])

def countDistance(x1,y1,x2,y2):
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def cDL(pos1,pos2):
	return countDistance(pos1[0],pos1[1],pos2[0],pos2[1])

def createFire():
	return Fire(random.randint(77,980),random.randint(25,660),fire_img1,fire_img2)

def removeWater(num):
	global player,currentGameStats
	if(gameSettings["usingWater"] and ("LEFT_SHIFT" in buttonsDown) and player.water > 1):
		player.water -= num
		currentGameStats["waterSpent"] += num

def mainMenu():
	window.blit(mainMenuImg,[0,0])
	window.blit(mm_titleImg,[185,0])
	for btn in mmButtons:
		btn.testForMouse()
		btn.render(window)

def settingsMenu():
	window.blit(settingsMenuImg,[0,0])
	for btn in seButtons:
		btn.testForMouse()
		btn.render(window)

def pre_game():
	window.blit(pre_gameMenuImg,[0,0])
	for btn in pgButtons:
		btn.testForMouse()
		btn.render(window)

def lose_menu():
	window.blit(ig_background_l,[0,0])
	returnFromLoseButton.testForMouse()
	returnFromLoseButton.render(window)
	putOutText = igFont.render(f"{currentGameStats['firesPutOut']}",True,(255,255,255))
	waterUsedText = igFont.render(f"{currentGameStats['waterSpent']}",True,(255,255,255))
	window.blit(putOutText,[387,250])
	window.blit(waterUsedText,[380,300])

def win_menu():
	window.blit(ig_background_w,[0,0])
	returnFromWinButton.testForMouse()
	returnFromWinButton.render(window)
	putOutText = igFont.render(f"{currentGameStats['firesPutOut']}",True,(255,255,255))
	waterUsedText = igFont.render(f"{currentGameStats['waterSpent']}",True,(255,255,255))
	window.blit(putOutText,[420,275])
	window.blit(waterUsedText,[420,225])

def game_cycle():
	global fireTick,fires,gameState,currentGameStats
	window.blit(ig_background,[0,0])
	if(len(fires) < gameSettings["loseOnXFires"]):
		if(fireTick >= gameSettings["fireSpreadSpeed"]):
			fires.append(createFire())
			fireTick = 0
		else:
			fireTick += 1
	else:
		gameState = 7

	if(len(fires) == 0):
		gameState = 6

	for fire in fires:
		fire.render(window)
		if(player.water > 5 and gameSettings["usingWater"]):
			if(cDL(player.getCenter(),fire.getCenter()) < 50):
				fires.remove(fire)
				player.water -= 5
				currentGameStats["waterSpent"] += 5
				currentGameStats["firesPutOut"] += 1
		elif(not gameSettings["usingWater"]):
			if(cDL(player.getCenter(),fire.getCenter()) < 50):
				fires.remove(fire)
				currentGameStats["firesPutOut"] += 1

	if(gameSettings["usingWater"]):
		window.blit(ig_waterDisp,[1114,654])
		if(cDL(player.getCenter(),[1114,654]) < 75 and player.water < 100):
			player.water += 2
		ratio = int((177)*(player.water / 100))
		waterSurface = pygame.Surface((ratio if ratio > 0 else 1,13))
		waterSurface.fill((0,0,255))
		window.blit(waterSurface,(1075,90))
		window.blit(ig_waterDisplay,[1050,80])

	player.render(window)



while True:
	window.fill((128,128,128))

	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
		if(event.type == pygame.KEYDOWN):
			if(event.__dict__["scancode"] == 225):
				buttonsDown.append("LEFT_SHIFT")
			buttonsDown.append(event.__dict__['unicode'].lower())
		if(event.type == pygame.KEYUP):
			if(event.__dict__["scancode"] == 225):
				buttonsDown.remove("LEFT_SHIFT")
			try:
				buttonsDown.remove(event.__dict__['unicode'].lower())
			except Exception:
				pass

	if(gameState == 4):
		if("w" in buttonsDown):
			player.y -= 5 * (3 if "LEFT_SHIFT" in buttonsDown and player.water > 1 else 1)
			removeWater(0.5)
		if("s" in buttonsDown):
			player.y += 5 * (3 if "LEFT_SHIFT" in buttonsDown and player.water > 1 else 1)
			removeWater(0.5)
		if("d" in buttonsDown):
			player.x += 5 * (3 if "LEFT_SHIFT" in buttonsDown and player.water > 1 else 1)
			removeWater(0.5)
		if("a" in buttonsDown):
			player.x -= 5 * (3 if "LEFT_SHIFT" in buttonsDown and player.water > 1 else 1)
			removeWater(0.5)
		if(player.x > windowSize[0] + player.imgSeq[0].get_size()[0]):
			player.x = -player.imgSeq[0].get_size()[0]
		if(player.x < -player.imgSeq[0].get_size()[0]):
			player.x = windowSize[0] + player.imgSeq[0].get_size()[0]
		if(player.y > windowSize[1] - player.imgSeq[0].get_size()[1]):
			player.y = windowSize[1] - player.imgSeq[0].get_size()[1]
		if(player.y < 0):
			player.y = 0

	if(gameState == 0):
		mainMenu()
	if(gameState == 2):
		settingsMenu()
	if(gameState == 1):
		pre_game()
	if(gameState == 4):
		game_cycle()
	if(gameState == 7):
		lose_menu()
	if(gameState == 6):
		win_menu()

	pygame.display.flip()