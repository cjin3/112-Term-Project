from cmu_graphics import *
import time
import math
import random

from button import *
from enemy import *
from tower import *
from projectile import *
from load import *

def onAppStart(app):
    app.scenes = ['Title Page', 'Game Menu', 'Map Editor', 'Campaign', 'Load Menu']
    app.levels = ['Endless']

    app.loadingDict = {'Title Page': loadTitlePage, 'Game Menu': loadGameMenu, 'Map Editor': loadMapEditor, 'Campaign': loadCampaign, 'Load Menu': loadLoadMenu, 'Endless': loadEndless}
    
    app.stepsPerSecond = 60
    app.loaded = False

    app.needMoreMoneyDraw = False
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
    app.money = 1000
    app.map = ENDLESS_MAP
    loadLevel(app)
    app.loaded = True
def loadLevel(app):
    #Towers, Enemies, and Projectiles
    app.healthBarSize = 5
    app.towers = []
    app.enemies = []
    app.projectiles = []

    app.showingRange = False
    app.placingTowers = False
    app.placement = None
    app.mouseLocation = (0,0)
    app.previewOpacity = 80
    app.needMoreMoneyDraw = False

    #Map
    app.cellSize = 40
    app.startCell = (0,0)
    app.endCell = (0,0)
    app.enemyPath = []
    loadMap(app)
    loadEnemyPath(app)
    print(app.enemyPath)

def loadMap(app):
    rows, cols = len(app.map), len(app.map[0])
    for row in range(rows):
        for col in range(cols):
            location = (col, row)
            cell = app.map[row][col]
            if cell == 'S': app.startCell = location
            elif cell == 'E': app.endCell = location
def loadEnemyPath(app):
    app.enemyPath = loadEnemyPathHelper(app, app.startCell, [], None)

def loadEnemyPathHelper(app, location, list, prevDirection):
    if app.map[location[1]][location[0]] == 'E':
        list.append(((location[0]*app.cellSize + app.cellSize/2, location[1]*app.cellSize + app.cellSize/2), prevDirection))
        return list
    else:
        left = (location[0]-1, location[1])
        right = (location[0]+1, location[1])
        up = (location[0], location[1]-1)
        down = (location[0], location[1]+1)
        
        if prevDirection != 'right' and isLegalCell(app, left) and (app.map[left[1]][left[0]] == 'P' or app.map[left[1]][left[0]] == 'E'): #check left
            list.append(((left[0]*app.cellSize + app.cellSize/2, left[1]*app.cellSize + app.cellSize/2), 'left'))
            return loadEnemyPathHelper(app, left, list, 'left')
        elif prevDirection != 'left' and isLegalCell(app, right) and (app.map[right[1]][right[0]] == 'P' or app.map[right[1]][right[0]] == 'E'): #check right
            list.append(((right[0]*app.cellSize + app.cellSize/2, right[1]*app.cellSize + app.cellSize/2), 'right'))
            return loadEnemyPathHelper(app, right, list, 'right')
        elif prevDirection != 'up' and isLegalCell(app, down) and (app.map[down[1]][down[0]] == 'P' or app.map[down[1]][down[0]] == 'E'): #check down
            list.append(((down[0]*app.cellSize + app.cellSize/2, down[1]*app.cellSize + app.cellSize/2), 'down'))
            return loadEnemyPathHelper(app, down, list, 'down')
        elif prevDirection != 'down' and isLegalCell(app, up) and (app.map[up[1]][up[0]] == 'P' or app.map[up[1]][up[0]] == 'E'): #check up
            list.append(((up[0]*app.cellSize + app.cellSize/2, up[1]*app.cellSize + app.cellSize/2), 'up'))
            return loadEnemyPathHelper(app, up, list, 'up')

def isLegalCell(app, position):
    numRows = app.height//app.cellSize
    numCols = app.width//app.cellSize
    if (position[0] < 0) or (position[0] > numCols): return False
    elif (position[1] < 0) or (position[1] > numRows): return False
    return True
        

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
        for tower in app.towers: #let towers spawn projectiles
            for enemy in app.enemies:
                if inRange(enemy, tower):
                    tower.checkAttack()
                    if (tower.canAttack and tower.attackingEnemy == None) or (tower.attackingEnemy == enemy and tower.canAttack):
                        towerType = tower.getType()
                        damage = tower.dealDamage(enemy)
                        projectile = Projectile(tower, enemy, tower.getPosition(), damage)
                        if towerType == 'Magic': projectile = MagicProjectile(tower, enemy, tower.getPosition(), damage)
                        elif towerType == 'Archer': projectile = ArcherProjectile(tower, enemy, tower.getPosition(), damage)
                        elif towerType == 'Bomb': projectile = BombProjectile(tower, enemy, tower.getPosition(), damage)
                        app.projectiles.append(projectile)
                        
        for projectile in app.projectiles: #move projectiles
            projectile.move()
        
        for enemy in app.enemies: #move enemies
            enemy.move(app.enemyPath)
        
        for tower in app.towers: #check if enemies have moved out of range
            enemy = tower.attackingEnemy
            if enemy != None:
                if not inRange(enemy, tower):
                    tower.attackingEnemy = None
                    tower.attacking = False

        for enemy in app.enemies: #hit enemies and remove projectiles that hit
            for i in range(len(app.projectiles)-1, -1, -1): 
                if hit(enemy, app.projectiles[i]):
                    dmg = app.projectiles[i].dmg
                    enemy.takeDamage(dmg[0], dmg[1])
                    app.projectiles.pop(i)
                elif outOfBoard(app, app.projectiles[i]): #remove projectiles out of board
                    app.projectiles.pop(i)

        for i in range(len(app.enemies)-1, -1, -1): #dead enemies die
            enemy = app.enemies[i]
            if enemy.getHealth() <= 0:
                app.enemies.pop(i)
                for tower in app.towers:
                    if tower.attackingEnemy == enemy:
                        tower.attackingEnemy = None
                        tower.attacking = False

def hit(enemy, projectile):
    return enemy.size + projectile.size >= distance(enemy.position[0], enemy.position[1], projectile.position[0], projectile.position[1])
def inRange(enemy, tower):
    return enemy.size + tower.range + tower.size >= distance(enemy.position[0], enemy.position[1], tower.position[0], tower.position[1])
def outOfBoard(app, projectile):
    location = projectile.getPosition()
    return (0 > location[0] or location[0] > app.width) or (0 > location[1] or location[1] > app.height)

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
    drawMap(app)
    label = 'p for placing towers, e for placing enemies'
    if app.placement == 'm': label = 'placing magic towers!'
    elif app.placement == 'a': label = 'placing archer towers!'
    elif app.placement == 'b': label = 'placing bomb towers!'
    elif app.placement == 'e': label = 'placing enemies!'
    drawLabel(label, app.height-100, app.width/2)

    for tower in app.towers:
        towerType = tower.getType()
        if towerType == 'Magic': drawMagicTower(app, tower, 100)
        elif towerType == 'Archer': drawArcherTower(app, tower, 100)
        elif towerType == 'Bomb': drawBombTower(app, tower, 100)
        if app.showingRange:
            showRange(app, tower)
    for enemy in app.enemies:
        drawEnemy(app, enemy)
    for projectile in app.projectiles:
        drawProjectile(app, projectile)
    

def drawMap(app):
    rows, cols = len(app.map), len(app.map[0])
    for row in range(rows):
        for col in range(cols):
            drawCell(app, app.map, row, col)
def drawCell(app, map, row, col):
    cell = map[row][col]
    location = (col*app.cellSize, row*app.cellSize)
    if cell == 'S':
        drawRect(location[0], location[1], app.cellSize, app.cellSize, fill='tan')
    elif cell == 'E':
        drawRect(location[0], location[1], app.cellSize, app.cellSize, fill='tan')
    elif cell == 'P':
        drawRect(location[0], location[1], app.cellSize, app.cellSize, fill='tan')
    elif cell == 0:
        drawRect(location[0], location[1], app.cellSize, app.cellSize, fill='limeGreen')
    elif cell == 1:
        drawRect(location[0], location[1], app.cellSize, app.cellSize, fill='lawnGreen')

def drawMagicTower(app, tower, opacity):
    position = tower.position
    size = MAGIC_SIZE
    drawCircle(position[0], position[1], size, fill='lightBlue', opacity=opacity)
def drawBombTower(app, tower, opacity):
    position = tower.position
    size = BOMB_SIZE
    drawCircle(position[0], position[1], size, fill='grey', opacity=opacity)
def drawArcherTower(app, tower, opacity):
    position = tower.position
    size = ARCHER_SIZE
    drawCircle(position[0], position[1], size, fill='brown', opacity=opacity)
def drawMagicPreview(app):
    position = app.mouseLocation
    size = MAGIC_SIZE
    if isLegalTowerPlacement(app, 'm', position):
        drawCircle(position[0], position[1], size, fill='lightBlue', opacity=app.previewOpacity)
    else:
        drawCircle(position[0], position[1], size, fill='red', opacity=app.previewOpacity)
def drawBombPreview(app):
    position = app.mouseLocation
    size = BOMB_SIZE
    if isLegalTowerPlacement(app, 'b', position):
        drawCircle(position[0], position[1], size, fill='grey', opacity=app.previewOpacity)
    else:
        drawCircle(position[0], position[1], size, fill='red', opacity=app.previewOpacity)
def drawArcherPreview(app):
    position = app.mouseLocation
    size = ARCHER_SIZE
    if isLegalTowerPlacement(app, 'a', position):
        drawCircle(position[0], position[1], size, fill='brown', opacity=app.previewOpacity)
    else:
        drawCircle(position[0], position[1], size, fill='red', opacity=app.previewOpacity)

def drawEnemy(app, enemy):
    position = enemy.position
    size = enemy.size
    topLeft = (position[0]-size, position[1]-app.healthBarSize/2-20)
    drawRect(topLeft[0], topLeft[1], size*2, app.healthBarSize, fill='red')
    maxHealth = Enemy.health[enemy.getType()]
    healthRemainingSize = size*2 * (enemy.getHealth()/maxHealth)
    drawRect(topLeft[0], topLeft[1], healthRemainingSize, app.healthBarSize, fill='green')
    drawCircle(position[0], position[1], size, fill='red')
def drawProjectile(app, projectile):
    position = projectile.getPosition()
    size = projectile.getSize()
    color = projectile.getColor()
    drawCircle(position[0], position[1], size, fill=color)
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
    if app.scene in app.levels:
        #draw side menu

        #previews
        if app.placement == 'm' and app.placingTowers: drawMagicPreview(app)
        elif app.placement == 'b' and app.placingTowers: drawBombPreview(app)
        elif app.placement == 'a' and app.placingTowers: drawArcherPreview(app)

        #need more money label
        if app.needMoreMoneyDraw and app.placingTowers: drawLabel('NEED MORE MONEY!', app.mouseLocation[0], app.mouseLocation[1]-50, size=20)
    
#button functions
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
#end button functions

def onKeyPress(app, keys):
    if 'k' in keys:
        app.loaded = True
        app.scene = "Game Menu"
    if 'r' in keys:
        app.loaded = True
        app.scene = 'Title Page'
    if app.scene in app.levels:
        if app.placingTowers:
            if 'm' in keys: app.placement = 'm'
            elif 'a' in keys: app.placement = 'a'
            elif 'b' in keys: app.placement = 'b'
        if 's' in keys:
            app.showingRange = True
        if 'e' in keys:
            app.placement = 'e'

def onKeyRelease(app, keys):
    if app.scene in app.levels:
        if 's' in keys:
            app.showingRange = False

def onMouseMove(app, mouseX, mouseY):
    if app.scene in app.levels:
        app.mouseLocation = (mouseX, mouseY)

def onMousePress(app, mouseX, mouseY):
    #check buttons
    for location in Button.buttonLocations.keys():
        if (app.scene == location[2]) and (location[0][0] <= mouseX <= location[1][0]) and (location[0][1] <= mouseY <= location[1][1]): #clicked button
            clicked = Button.buttonLocations[location]
            Button.buttonFunctions[clicked](app)
            return
    if app.scene in app.levels:
        position = (mouseX, mouseY)
        app.mouseLocation = position
        if app.placement == 'm' and app.placingTowers and isLegalTowerPlacement(app, 'm', position) and hasMoney(app, MAGIC_LVL0_COST):
            newTower = Magic('Magic', position, 0)
            app.towers.append(newTower)
        elif app.placement == 'b' and app.placingTowers and isLegalTowerPlacement(app, 'b', position) and hasMoney(app, BOMB_LVL0_COST):
            newTower = Bomb('Bomb', position, 0)
            app.towers.append(newTower)
        elif app.placement == 'a' and app.placingTowers and isLegalTowerPlacement(app, 'a', position) and hasMoney(app, ARCHER_LVL0_COST):
            newTower = Archer('Archer', position, 0)
            app.towers.append(newTower)
        elif app.placement == 'e':
            startLocation = (app.startCell[0] * app.cellSize + app.cellSize/2, app.startCell[1] * app.cellSize + app.cellSize/2)
            newEnemy = Enemy('Goblin', startLocation, startLocation, app.enemyPath)
            app.enemies.append(newEnemy)
        else:
            app.placingTowers = True
        
def isLegalTowerPlacement(app, type, position):
    size = 0
    if type == 'a': size = ARCHER_SIZE
    elif type == 'b': size = BOMB_SIZE
    elif type == 'm': size = MAGIC_SIZE
    
    if (position[0] + size > app.width) or (position[0] - size < 0): return False
    elif (position[1] + size > app.height) or (position[1] - size < 0): return False

    topPosition = (position[0], position[1] + size)
    botPosition = (position[0], position[1] - size)
    leftPosition = (position[0] - size, position[1])
    rightPosition = (position[0] + size, position[1])
    if getCell(app, topPosition) != 1 or getCell(app, botPosition) != 1 or getCell(app, leftPosition) != 1 or getCell(app, rightPosition) != 1: return False

    for tower in app.towers:
        towerSize = tower.getSize()
        towerPosition = tower.getPosition()
        if intersectingCircles(position, towerPosition, towerSize, size):
            return False

    return True
def hasMoney(app, cost):
    if app.money >= cost:
        app.money -= cost
        return True
    app.needMoreMoneyDraw = True
    return False
def getCell(app, position):
    location = (position[0]//app.cellSize, position[1]//app.cellSize)
    return app.map[location[1]][location[0]]
def intersectingCircles(position1, position2, size1, size2):
    return distance(position1[0], position1[1], position2[0], position2[1]) <= (size1 + size2)

def main():
    runApp()

main()