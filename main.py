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
    app.title = 'TBD'
    app.scenes = ['Title Page', 'Game Menu', 'Map Editor', 'Campaign', 'Load Menu']
    app.levels = ['Endless', 'Tutorial']

    app.loadingDict = {'Title Page': loadTitlePage, 'Game Menu': loadGameMenu, 'Map Editor': loadMapEditor, 'Campaign': loadCampaign, 'Load Menu': loadLoadMenu, 'Endless': loadEndless, 'Tutorial': loadTutorial}
    
    app.stepsPerSecond = 60
    app.loaded = False

    app.needMoreMoneyDraw = False
    app.mouseLocation = (0,0)
    app.fillHover = 'gray'
    app.fillNorm = 'black'
    app.doneTutorial = False

    loadImages(app)
    restart(app)

def loadImages(app):
    app.heart = 'heart.png'
    app.arrow = 'arrow.png'
def restart(app):
    app.prevScene = 'Title Page'
    app.scene = 'Title Page'
    app.paused = False
    app.gameOver = False
    app.win = False
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
    app.waves = ENDLESS_WAVES
    app.health = 1
    
    loadLevel(app)
    app.loaded = True
def loadTutorial(app):
    app.width = 1200
    app.height = 800
    app.money = 1000
    app.map = TUTORIAL_MAP
    app.waves = TUTORIAL_WAVES
    app.health = 100

    app.welcomeTxt = False
    app.waveTxt = False
    app.enemiesTxt = False
    app.glhf = False
    app.checkpoints = [app.welcomeTxt, app.waveTxt, app.enemiesTxt, app.glhf]

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
    app.previewOpacity = 80
    app.needMoreMoneyDraw = False
    app.drawTowerUpgrade = (False, None)
    app.lastSpawnTime = 0
    app.spawnTime = 0.5
    app.startWave = False
    app.wave = 0
    app.lastSpawn = 0
    app.finalWave = False

    #Map
    app.cellSize = 40
    app.startCell = (0,0)
    app.endCell = (0,0)
    app.enemyPath = []
    loadMap(app)
    loadEnemyPath(app)

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


def checkHover(app, button):
    location = button.getLocation()
    if (app.scene == location[2]) and (location[0][0] <= app.mouseLocation[0] <= location[1][0]) and (location[0][1] <= app.mouseLocation[1] <= location[1][1]):
        button.setFillHover()
    else:
        button.setFillNorm()
def checkChangeScene(app):
    if app.scene != app.prevScene:
        app.prevScene = app.scene
        app.loadingDict[app.scene](app)
        print(f'current scene: {app.scene}')

def takeStep(app):
    if app.scene in app.levels:
        if app.wave >= len(app.waves):
            app.finalWave = True
            app.startWave = False
            if app.enemies == []:
                if app.scene == 'Tutorial' and app.doneTutorial == False:
                    app.doneTutorial = True
                app.win = True
            

        if app.startWave: #spawn waves
            wave = app.waves[app.wave]
            for i in range(app.lastSpawn, len(wave)): 
                currTime = time.time()
                if currTime - app.lastSpawnTime >= app.spawnTime:
                    enemy = wave[i]
                    startLocation = (app.startCell[0] * app.cellSize + app.cellSize/2, app.startCell[1] * app.cellSize + app.cellSize/2)
                    newEnemy = Enemy(enemy, startLocation, startLocation, app.enemyPath)
                    app.lastSpawn += 1
                    app.lastSpawnTime = currTime
                    app.enemies.append(newEnemy)
                if app.lastSpawn == len(wave):
                    app.startWave = False
                    app.lastSpawn = 0
                    app.wave += 1


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
                money = enemy.getMoney()
                app.money += money
                app.enemies.pop(i)
                for tower in app.towers:
                    if tower.attackingEnemy == enemy:
                        tower.attackingEnemy = None
                        tower.attacking = False
        
        for i in range(len(app.enemies)-1, -1, -1): #enemies at the end disappear, lose health
            enemy = app.enemies[i]
            if enemy.getFinished():
                app.health -= enemy.getHealthLost()
                app.enemies.pop(i)
                for tower in app.towers:
                    if tower.attackingEnemy == enemy:
                        tower.attackingEnemy = None
                        tower.attacking = False

        if app.health <= 0: 
            print('gameover!')
            app.gameOver = True

def mouseHover(app, button):
    location = button.getLocation()
    topLeft, botRight = location[0], location[1]
    return (topLeft[0] <= app.mouseLocation[0] <= botRight[0]) and (topLeft[1] <= app.mouseLocation[1] <= botRight[1])
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
    playButton = Button(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2, app.width/2+buttonWidth/2, app.height/2+buttonHeight/2, 'Title Page', pressPlay, app.fillHover, app.fillNorm)
    checkHover(app, playButton)
    drawRect(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2, buttonWidth, buttonHeight, fill=playButton.getFill(), border=app.fillNorm)
    drawLabel('PLAY', app.width/2, app.height/2, fill=app.buttonTextFill)

    #Load button
    buttonWidth = 200
    buttonHeight = 100
    gap = 150
    loadButton = Button(app.width/2-buttonHeight/2, app.height/2-buttonHeight/2 + gap, app.width/2+buttonWidth/2, app.height/2+buttonHeight/2 + gap, 'Title Page', pressLoad, app.fillHover, app.fillNorm)
    checkHover(app, loadButton)
    drawRect(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2 + gap, buttonWidth, buttonHeight, fill=loadButton.getFill(), border=app.fillNorm)
    drawLabel('LOAD', app.width/2, app.height/2 + gap, fill=app.buttonTextFill)
def drawGameMenu(app):
    #Campaign button
    buttonWidth = 250
    buttonHeight = 500
    campaignButton = Button(app.width/2-buttonWidth-100, app.height/2-buttonHeight/2, app.width/2, app.height/2+buttonHeight/2,  'Game Menu', pressCampaign, app.fillHover, app.fillNorm)
    checkHover(app, campaignButton)
    drawRect(app.width/2-buttonWidth-100, app.height/2-buttonHeight/2, buttonWidth, buttonHeight, fill=campaignButton.getFill(), border=app.fillNorm )
    drawLabel('Campaign', app.width/2-buttonWidth/2-100, app.height/2, fill=app.buttonTextFill)

    #Map Editor button
    buttonWidth = 250
    buttonHeight = 500
    mapEditorButton = Button(app.width/2+buttonWidth+100, app.height/2-buttonHeight/2, app.width/2+2*buttonWidth, app.height/2+buttonHeight/2, 'Game Menu', pressMapEditor, app.fillHover, app.fillNorm)
    checkHover(app, mapEditorButton)
    drawRect(app.width/2+buttonWidth+100, app.height/2-buttonHeight/2, buttonWidth, buttonHeight, fill='white')
    drawLabel('Map Editor', app.width/2+buttonWidth/2, app.height/2, fill=app.buttonTextFill)
def drawCampaign(app):
    buttonWidth = 500
    buttonHeight = 500
    endlessButton = Button(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2, app.width/2+buttonWidth/2, app.height/2+buttonHeight/2, 'Campaign', pressEndless, app.fillHover, app.fillNorm)
    checkHover(app, endlessButton)
    drawRect(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2, buttonWidth, buttonHeight, fill=app.buttonFill)
    drawLabel('Endless Level', app.width/2, app.height/2, fill=app.buttonTextFill)
def drawEndless(app):
    drawMap(app)

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
    
    if not app.startWave and app.loaded and not app.finalWave: #wave button
        startWave = Button(app.startCell[0]*app.cellSize, app.startCell[1]*app.cellSize, app.startCell[0]*app.cellSize+app.cellSize, app.startCell[1]*app.cellSize+app.cellSize, 'Endless', pressStartWave, 'crimson', 'fireBrick')
        checkHover(app, startWave)
        drawCircle(app.startCell[0]*app.cellSize + app.cellSize/2, app.startCell[1]*app.cellSize + app.cellSize/2, app.cellSize/3, fill=startWave.getFill(), border=startWave.fillNorm)
    
    #money
    drawCircle(25, 25, 20, fill='gold')
    drawCircle(25, 25, 15, fill='yellow')
    drawLabel(f'{app.money}', 75, 25, size=20)

    #heart
    drawImage(app.heart, 0, 50, width=50, height=50)
    drawLabel(f'{app.health}', 75, 75, size=20)

    #draw side menu
    if not app.paused:
        if app.placingTowers and not mouseInSideMenu(app): drawSideMenu(app)
        #previews
        if app.placement == 'm' and app.placingTowers: drawMagicPreview(app)
        elif app.placement == 'b' and app.placingTowers: drawBombPreview(app)
        elif app.placement == 'a' and app.placingTowers: drawArcherPreview(app)

        #need more money label
        if app.needMoreMoneyDraw and app.placingTowers: drawLabel('NEED MORE MONEY!', app.mouseLocation[0], app.mouseLocation[1]-50, size=20)
        
        #upgrade tower menu
        if app.drawTowerUpgrade[0]: drawTowerUpgrade(app)

        #game over
        if app.gameOver: drawGameOver(app)

        if app.win: drawWin(app)

def drawTutorial(app):
    drawMap(app)
    
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
    
    if not app.startWave and app.loaded and not app.finalWave: #wave button
        startWave = Button(app.startCell[0]*app.cellSize, app.startCell[1]*app.cellSize, app.startCell[0]*app.cellSize+app.cellSize, app.startCell[1]*app.cellSize+app.cellSize, 'Tutorial', pressStartWave, 'crimson', 'fireBrick')
        checkHover(app, startWave)
        drawCircle(app.startCell[0]*app.cellSize + app.cellSize/2, app.startCell[1]*app.cellSize + app.cellSize/2, app.cellSize/3, fill=startWave.getFill(), border=startWave.fillNorm)

    #draw side menu
    if not app.paused:
        if app.placingTowers and not mouseInSideMenu(app): drawSideMenu(app)
        #previews
        if app.placement == 'm' and app.placingTowers: drawMagicPreview(app)
        elif app.placement == 'b' and app.placingTowers: drawBombPreview(app)
        elif app.placement == 'a' and app.placingTowers: drawArcherPreview(app)

        #need more money label
        if app.needMoreMoneyDraw and app.placingTowers: drawLabel('NEED MORE MONEY!', app.mouseLocation[0], app.mouseLocation[1]-50, size=20)
        
        #upgrade tower menu
        if app.drawTowerUpgrade[0]: drawTowerUpgrade(app)

        #game over
        if app.gameOver: drawGameOver(app)
        if app.win: drawWin(app)

    #money
    drawCircle(25, 25, 20, fill='gold')
    drawCircle(25, 25, 15, fill='yellow')
    drawLabel(f'{app.money}', 75, 25, size=20)

    #heart
    drawImage(app.heart, 0, 50, width=50, height=50)
    drawLabel(f'{app.health}', 75, 75, size=20)

    drawTutorialStory(app)

def drawTutorialStory(app):
    fillColor = 'aqua'
    if not app.checkpoints[0]:
        
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        gap = 50
        drawLabel(f'Welcome to {app.title}!', app.width/2, app.height/2-gap*5, size=50, fill=fillColor)
        drawLabel(f'{app.title} is a tower defense game!', app.width/2, app.height/2+0*gap, size=30, fill=fillColor)
        drawLabel(f'Enemies spawn at the red circle.', app.width/2, app.height/2+gap, size=30, fill=fillColor)
        drawLabel(f'Prevent them from getting to the end with towers!', app.width/2, app.height/2+2*gap, size=30, fill=fillColor)
        drawLabel(f'If enemies reach the end, you lose health', app.width/2, app.height/2+3*gap, size=30, fill=fillColor)
        drawLabel(f'If you have no more health, you lose the game!', app.width/2, app.height/2+4*gap, size=30, fill=fillColor)

        drawImage(app.arrow, 50, 9*app.cellSize)
        drawLabel(f'Enemies spawn here!', 75, 8*app.cellSize, fill=fillColor)

        drawImage(app.arrow, 27*app.cellSize, 9*app.cellSize, rotateAngle=180)
        drawLabel(f'Stop enemies from getting here!', 27*app.cellSize, 8*app.cellSize, fill=fillColor)

        drawImage(app.arrow, 90, 1.5*app.cellSize)
        drawLabel(f'Your health', 120, 2.5*app.cellSize, fill=fillColor)
    
    elif not app.checkpoints[1]:
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        gap = 50
        drawLabel(f'You can use money to place towers.', app.width/2, app.height/2+0*gap, size=30, fill=fillColor)
        drawLabel(f'Enemies drop money upon defeat.', app.width/2, app.height/2+1*gap, size=30, fill=fillColor)
        drawLabel(f'Place towers by clicking anywhere on the map.', app.width/2, app.height/2+2*gap, size=30, fill=fillColor)
        drawLabel(f'Press the red button to spawn the next wave of enemies!', app.width/2, app.height/2+3*gap, size=30, fill=fillColor)

        drawImage(app.arrow, 90, 0.5*app.cellSize)
        drawLabel(f'Your money', 120, 1.5*app.cellSize, fill=fillColor)

        drawImage(app.arrow, 50, 9*app.cellSize)
        drawLabel(f'Press here to spawn enemies!', 90, 8*app.cellSize, fill=fillColor)
    
    elif not app.checkpoints[2]:
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        gap = 50
        drawLabel(f'There are different kinds of enemies:', app.width/2, app.height/2-2*gap, size=30, fill=fillColor)
        
        drawCircle(app.width/2, app.height/2, Enemy.size['Goblin'], fill='red')
        drawLabel('Red is the basic enemy', app.width/2, app.height/2+50, size=16, fill=fillColor)
        drawCircle(app.width/2-350, app.height/2, Enemy.size['Purple'], fill='purple')
        drawLabel('Purple has lots of health and takes less damage from physical', app.width/2-350, app.height/2+50, size=16, fill=fillColor)
        drawCircle(app.width/2+350, app.height/2, Enemy.size['Yellow'], fill='yellow')
        drawLabel('Yellow moves fast and takes less damage from magic', app.width/2+350, app.height/2+50, size=16, fill=fillColor)

    elif not app.checkpoints[3]:
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        gap = 50
        drawLabel(f'Good luck and have fun!', app.width/2, app.height/2+0*gap, size=30, fill=fillColor)
        


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
    drawCircle(position[0], position[1], size, fill='gray', opacity=opacity)
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
        drawCircle(position[0], position[1], size, fill='gray', opacity=app.previewOpacity)
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
    if enemy.getType() == 'Goblin':
        drawCircle(position[0], position[1], size, fill='red')
    elif enemy.getType() == 'Purple':
        drawCircle(position[0], position[1], size, fill='purple')
    elif enemy.getType() == 'Yellow':
        drawCircle(position[0], position[1], size, fill='yellow')
def drawProjectile(app, projectile):
    position = projectile.getPosition()
    size = projectile.getSize()
    color = projectile.getColor()
    drawCircle(position[0], position[1], size, fill=color)
def showRange(app, tower):
    range = tower.getRange()
    size = tower.size
    position = tower.getPosition()
    drawCircle(position[0], position[1], range+size, fill='blue', opacity=20)
def drawSideMenu(app):
    opacity = 70
    drawRect(1000, 0, 200, 800, fill='brown', opacity=opacity)
    drawLabel('PICK A TOWER', 1100, 100, size=20)

    #draw magic tower
    drawLabel('Press "m" for Magic', 1100, 150, size=16)
    drawCircle(1100, 200, MAGIC_SIZE, fill='lightBlue', opacity=100)
    drawLabel('200 coin', 1100, 200)

    #draw bomb tower
    drawLabel('Press "b" for Bomb', 1100, 300, size=16)
    drawCircle(1100, 350, BOMB_SIZE, fill='gray', opacity=100)
    drawLabel('320 coin', 1100, 350)

    #draw archer tower
    drawLabel('Press "a" for Archer', 1100, 450, size=16)
    drawCircle(1100, 500, ARCHER_SIZE, fill='brown', opacity=100)
    drawLabel('280 coin', 1100, 500)

def drawTowerUpgrade(app):
    pass
def drawGameOver(app, scene):
    drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
    drawLabel('GAME OVER!', app.width/2, app.height/2-100, size=100)

    restartButton = Button(app.width/2-100, app.height/2, app.width/2+100, app.height/2+100, app.scene, pressRestartEndless, app.fillHover, app.fillNorm)
    checkHover(app, restartButton)
    drawRect(app.width/2-100, app.height/2, 200, 100, fill=restartButton.getFill(), border=app.fillNorm)
    drawLabel('RESTART', app.width/2, app.height/2+50, size=20, fill=app.buttonTextFill)

    mainMenuButton = Button(app.width/2-100, app.height/2+150, app.width/2+100, app.height/2+250, app.scene, pressMainMenuEndless, app.fillHover, app.fillNorm)
    checkHover(app, mainMenuButton)
    drawRect(app.width/2-100, app.height/2+150, 200, 100, fill=mainMenuButton.getFill(), border=app.fillNorm)
    drawLabel('MAIN MENU', app.width/2, app.height/2+200, size=20, fill=app.buttonTextFill)
def drawPauseMenu(app, scene):
    drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
    drawLabel('Paused', app.width/2, app.height/2-100, size=100)

    drawLabel('Press "p" to unpause', app.width/2, app.height/2+50, size=50)

    mainMenuButton = Button(app.width/2-100, app.height/2+150, app.width/2+100, app.height/2+250, app.scene, pressMainMenuEndless, app.fillHover, app.fillNorm)
    checkHover(app, mainMenuButton)
    drawRect(app.width/2-100, app.height/2+150, 200, 100, fill=mainMenuButton.getFill(), border=app.fillNorm)
    drawLabel('MAIN MENU', app.width/2, app.height/2+200, size=20, fill=app.buttonTextFill)
def drawWin(app):
    drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
    drawLabel('YOU WIN!', app.width/2, app.height/2-100, size=100)

    restartButton = Button(app.width/2-100, app.height/2, app.width/2+100, app.height/2+100, app.scene, pressRestartEndless, app.fillHover, app.fillNorm)
    checkHover(app, restartButton)
    drawRect(app.width/2-100, app.height/2, 200, 100, fill=restartButton.getFill(), border=app.fillNorm)
    drawLabel('RESTART', app.width/2, app.height/2+50, size=20, fill=app.buttonTextFill)

    mainMenuButton = Button(app.width/2-100, app.height/2+150, app.width/2+100, app.height/2+250, app.scene, pressMainMenuEndless, app.fillHover, app.fillNorm)
    checkHover(app, mainMenuButton)
    drawRect(app.width/2-100, app.height/2+150, 200, 100, fill=mainMenuButton.getFill(), border=app.fillNorm)
    drawLabel('MAIN MENU', app.width/2, app.height/2+200, size=20, fill=app.buttonTextFill)

def redrawAll(app):
    if app.loaded:
        if app.scene == 'Title Page' and app.loaded: drawTitlePage(app)
        elif app.scene == "Game Menu" and app.loaded: drawGameMenu(app)
        elif app.scene == "Load Menu" and app.loaded: drawLoadMenu(app)
        elif app.scene == "Campaign" and app.loaded: drawCampaign(app)
        elif app.scene == "Map Builder" and app.loaded: drawMapBuilder(app)
        elif app.scene == 'Endless' and app.loaded: drawEndless(app)
        elif app.scene == 'Tutorial' and app.loaded: drawTutorial(app)            

def mouseInSideMenu(app):
    return (1000 <= app.mouseLocation[0] <= 1200) and (0 <= app.mouseLocation[1] <= 800)

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
    if app.doneTutorial:
        app.scene = 'Endless'
        app.loaded = False
        print('pressed endless')
    else:
        print('load tutorial')
        app.scene = 'Tutorial'
        app.loaded = False
def pressMapEditor(app): 
    app.scene = 'Map Editor'
    app.loaded = False
def pressRestartEndless(app):
    if app.scene == 'Tutorial':
        loadTutorial(app)
    elif app.scene == 'Endless':
        loadEndless(app)
    app.gameOver = False
    app.win = False
    print(app.enemies)
    print(app.gameOver)
def pressStartWave(app):
    app.startWave = True
def pressMainMenuEndless(app):
    restart(app)
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
        if 'p' in keys:
            app.paused = not app.paused

def onKeyRelease(app, keys):
    if app.scene in app.levels:
        if 's' in keys:
            app.showingRange = False

def onMouseMove(app, mouseX, mouseY):
    app.mouseLocation = (mouseX, mouseY)

def onMousePress(app, mouseX, mouseY):
    #check buttons
    if app.scene == 'Tutorial':
        for i in range(len(app.checkpoints)):
            if not app.checkpoints[i]:
                app.checkpoints[i] = True
                if app.paused: 
                    app.paused = False
                return

    for location in Button.buttonLocations.keys():
        if (app.scene == location[2]) and (location[0][0] <= mouseX <= location[1][0]) and (location[0][1] <= mouseY <= location[1][1]): #clicked button
            clicked = Button.buttonLocations[location]
            Button.buttonFunctions[clicked](app)
            return
                
    if app.scene in app.levels:
        position = (mouseX, mouseY)
        app.mouseLocation = position
        for tower in app.towers:
            if clickedTower(tower, position):
                app.drawTowerUpgrade = (True, tower)
        if app.placement == 'm' and app.placingTowers and isLegalTowerPlacement(app, 'm', position) and hasMoney(app, MAGIC_LVL0_COST):
            newTower = Magic('Magic', position, 0)
            app.towers.append(newTower)
        elif app.placement == 'b' and app.placingTowers and isLegalTowerPlacement(app, 'b', position) and hasMoney(app, BOMB_LVL0_COST):
            newTower = Bomb('Bomb', position, 0)
            app.towers.append(newTower)
        elif app.placement == 'a' and app.placingTowers and isLegalTowerPlacement(app, 'a', position) and hasMoney(app, ARCHER_LVL0_COST):
            newTower = Archer('Archer', position, 0)
            app.towers.append(newTower)
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
def clickedTower(tower, position):
    towerPosition = tower.getPosition()
    towerSize = tower.getSize()
    return (towerPosition[0] - towerSize <= position[0] <= towerPosition[0] + towerSize) and (towerPosition[1] - towerSize <= position[1] <= towerPosition[1] + towerSize)

def main():
    runApp()

main()