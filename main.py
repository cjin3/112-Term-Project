from cmu_graphics import *
import time
import math
import random

from button import *
from enemy import *
from tower import *
from load import *

def onAppStart(app):
    app.scenes = ['Title Page', 'Game Menu', 'Map Editor', 'Campaign', 'Load Menu']
    app.levels = ['Endless']

    app.loadingDict = {'Title Page': loadTitlePage, 'Game Menu': loadGameMenu, 'Map Editor': loadMapEditor, 'Campaign': loadCampaign, 'Load Menu': loadLoadMenu, 'Endless': loadEndless}
    
    app.stepsPerSecond = 5
    app.loaded = False
    restart(app)

def restart(app):
    app.prevScene = 'Title Page'
    app.scene = 'Title Page'
    app.paused = False
    app.gameOver = False
    app.placement = None    
    loadTitlePage(app)
def loadTitlePage(app):
    app.width = 1200
    app.height = 800
    app.buttonFill = 'blue'
    app.buttonTextFill = 'white'
    app.loaded = True
def loadGameMenu(app):
    app.width = 1200
    app.height = 800
    app.buttonFill = 'black'
    app.buttonTextFill = 'white'
    app.loaded = True
def loadMapEditor(app):
    app.width = 1200
    app.height = 800
    app.loaded = True
def loadCampaign(app):
    app.width = 1200
    app.height = 800
    app.loaded = True
def loadLoadMenu(app):
    app.width = 1200
    app.height = 800
    app.loaded = True
def loadEndless(app):
    app.width = 1200
    app.height = 800
    app.map = ENDLESS_MAP
    app.placement = None
    app.towers = []
    app.enemies = []
    app.showingRange = False
    app.loaded = True

def onStep(app):
    checkChangeScene(app)
    if not app.paused and not app.gameOver:
        takeStep(app)

def checkChangeScene(app):
    if app.scene != app.prevScene:
        app.prevScene = app.scene
        app.loadingDict[app.scene](app)
        print(f'current scene: {app.scene}')

def takeStep(app):
    if app.scene in app.levels:  
        
        for tower in app.towers: #let towers attack
            for enemy in app.enemies:
                if inRange(enemy, tower):
                    if (not tower.attacking and tower.attackingEnemy == None) or tower.attackingEnemy == enemy:
                        damage = tower.dealDamage(enemy)
                        enemy.takeDamage(damage[0], damage[1])
                        print(enemy.getHealth())

        for i in range(len(app.enemies)-1, -1, -1): #dead enemies die
            enemy = app.enemies[i]
            if enemy.getHealth() <= 0:
                app.enemies.pop(i)
                for tower in app.towers:
                    if tower.attackingEnemy == enemy:
                        tower.attackingEnemy = None
                        tower.attacking = False

def inRange(enemy, tower):
    return enemy.size + tower.range + tower.size >= distance(enemy.position[0], enemy.position[1], tower.position[0], tower.position[1])

def drawTitlePage(app):
    drawLabel("TITLE", app.width/2, app.height/2-150, size=100)

    #Play button
    buttonWidth = 200
    buttonHeight = 100
    playButton = Button(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2, app.width/2+buttonWidth/2, app.height/2+buttonHeight/2, 'Title Page', pressPlay)
    drawRect(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2, buttonWidth, buttonHeight, fill=app.buttonFill)
    drawLabel('PLAY', app.width/2, app.height/2, fill=app.buttonTextFill)

    #Load button
    buttonWidth = 200
    buttonHeight = 100
    gap = 150
    loadButton = Button(app.width/2-buttonHeight/2, app.height/2-buttonHeight/2 + gap, app.width/2+buttonWidth/2, app.height/2+buttonHeight/2 + gap, 'Title Page', pressLoad)
    drawRect(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2 + gap, buttonWidth, buttonHeight, fill=app.buttonFill)
    drawLabel('LOAD', app.width/2, app.height/2 + gap, fill=app.buttonTextFill)

def drawGameMenu(app):
    #Campaign button
    buttonWidth = 250
    buttonHeight = 500
    campaignButton = Button(app.width/2-buttonWidth-100, app.height/2-buttonHeight/2, app.width/2, app.height/2+buttonHeight/2,  'Game Menu', pressCampaign)
    drawRect(app.width/2-buttonWidth-100, app.height/2-buttonHeight/2, buttonWidth, buttonHeight, fill=app.buttonFill)
    drawLabel('Campaign', app.width/2-buttonWidth/2-100, app.height/2, fill=app.buttonTextFill)

    #Map Editor button
    buttonWidth = 250
    buttonHeight = 500
    mapEditorButton = Button(app.width/2+buttonWidth+100, app.height/2-buttonHeight/2, app.width/2+2*buttonWidth, app.height/2+buttonHeight/2, 'Game Menu', pressMapEditor)
    drawRect(app.width/2+buttonWidth+100, app.height/2-buttonHeight/2, buttonWidth, buttonHeight, fill=app.buttonFill)
    drawLabel('Map Editor', app.width/2+buttonWidth/2, app.height/2, fill=app.buttonTextFill)

def drawCampaign(app):
    buttonWidth = 500
    buttonHeight = 500
    endlessButton = Button(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2, app.width/2+buttonWidth/2, app.height/2+buttonHeight/2, 'Campaign', pressEndless)
    drawRect(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2, buttonWidth, buttonHeight, fill=app.buttonFill)
    drawLabel('Endless Level', app.width/2, app.height/2, fill=app.buttonTextFill)
def drawEndless(app):
    label = 'p for placing towers, e for placing enemies'
    if app.placement == 'p': label = 'placing towers!'
    elif app.placement == 'e': label = 'placing enemies!'
    drawLabel(label, app.height-100, app.width/2)

    for tower in app.towers:
        drawTower(app, tower)
        if app.showingRange:
            showRange(app, tower)
    for enemy in app.enemies:
        drawEnemy(app, enemy)
    
    #drawMap(app)



def drawMap(app):
    rows, cols = len(app.map), len(app.map[0])
    for row in rows:
        for col in cols:
            drawCell(app.map, row, col)
 
def drawCell(map, row, col): #FINISH THIS
    cell = map[row][col]

def drawTower(app, tower):
    position = tower.position
    size = tower.size
    drawCircle(position[0], position[1], size, fill='gray')
def drawEnemy(app, enemy):
    position = enemy.position
    size = enemy.size
    drawCircle(position[0], position[1], size, fill='red')
def showRange(app, tower):
    range = tower.getRange()
    size = tower.size
    position = tower.getPosition()
    drawCircle(position[0], position[1], range+size, fill='blue', opacity=30)

def redrawAll(app):
    if app.scene == 'Title Page' and app.loaded: drawTitlePage(app)
    elif app.scene == "Game Menu" and app.loaded: drawGameMenu(app)
    elif app.scene == "Load Menu" and app.loaded: drawLoadMenu(app)
    elif app.scene == "Campaign" and app.loaded: drawCampaign(app)
    elif app.scene == "Map Builder" and app.loaded: drawMapBuilder(app)
    elif app.scene == 'Endless' and app.loaded: drawEndless(app)

def pressPlay(app): 
    app.scene = 'Game Menu'
    app.loaded = False
    print('pressed play')
def pressLoad(app): 
    app.scene = "Load Menu"
    app.loaded = False
def pressCampaign(app): 
    app.scene = 'Campaign'
    app.loaded = False
    print('pressed campaign')
def pressEndless(app): 
    app.scene = 'Endless'
    app.loaded = False
    print('pressed endless')
def pressMapEditor(app): 
    app.scene = 'Map Editor'
    app.loaded = False

def onKeyPress(app, keys):
    if 'k' in keys:
        app.loaded = True
        app.scene = "Game Menu"
    if 'r' in keys:
        app.loaded = True
        app.scene = 'Title Page'
    if app.scene == 'Endless':
        if 'p' in keys:
            print('placing towers!')
            app.placement = 'p'
        elif 'e' in keys:
            print('placing enemies!')
            app.placement = 'e'
        if 's' in keys:
            print('showing range')
            app.showingRange = True

def onKeyRelease(app, keys):
    if app.scene == 'Endless':
        if 's' in keys:
            app.showingRange = False

def onMousePress(app, mouseX, mouseY):
    #check buttons
    for location in Button.buttonLocations.keys():
        if (app.scene == location[2]) and (location[0][0] <= mouseX <= location[1][0]) and (location[0][1] <= mouseY <= location[1][1]): #clicked button
            clicked = Button.buttonLocations[location]
            Button.buttonFunctions[clicked](app)
            return
    if app.scene in app.levels:
        if app.placement == 'p':
            newTower = Tower('m', 0, (mouseX, mouseY))
            app.towers.append(newTower)
        elif app.placement == 'e':
            newEnemy = Enemy('Goblin', (mouseX, mouseY))
            app.enemies.append(newEnemy)


def main():
    runApp()

main()