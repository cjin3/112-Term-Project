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
    print(time.time())
    app.titleName = 'BTD'
    app.scenes = ['Title Page', 'Game Menu', 'Map Editor', 'Campaign', 'Load Menu']
    app.levels = ['Endless', 'Tutorial', 'Load']

    app.loadingDict = {'Title Page': loadTitlePage, 'Game Menu': loadGameMenu, 'Map Editor': loadMapEditor, 'Campaign': loadCampaign, 'Load Menu': loadLoadMenu, 'Endless': loadEndless, 'Tutorial': loadTutorial, 'Load': loadLoad}
    
    app.stepsPerSecond = 60
    app.loaded = False

    app.needMoreMoneyDraw = False
    app.mouseLocation = (0,0)
    app.fillHover = 'gray'
    app.fillNorm = 'black'
    app.doneTutorial = False

    app.smallRadius = 15
    app.largeRadius = 25

    app.cellSize = 40

    loadImages(app)
    loadFiles(app)
    restart(app)
def loadFiles(app):
    app.save1 = 'save1.txt'
    app.save2 = 'save2.txt'
def loadImages(app):
    app.heart = 'heart.png'
    app.arrow = 'arrow.png'
    app.bricks = 'brick.png'
    app.title = 'title.png'
    app.torch = 'torch.png'
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
    app.map = MAP_EDITOR_MAP
    app.width = 1500
    app.height = 800

    app.selectedBlock = None

    app.startCell = None
    app.endCell = None
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
def loadLoad(app):
    app.width = 1200
    app.height = 800
    app.money = 1000
    app.waves = ENDLESS_WAVES
    app.health = 1
    
    loadLevel(app)
    app.loaded = True

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
    if app.scene == 'Map Editor':
        if findStart(app, app.map) and app.selectedBlock == 'S':
            app.selectedBlock = None
        if findEnd(app, app.map) and app.selectedBlock == 'E':
            app.selectedBlock = None

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
def findEnd(app, map):
    rows, cols = len(map), len(map[0])
    for row in range(rows):
        for col in range(cols):
            if map[row][col] == 'E':
                return True
    return False
def findStart(app, map):
    rows, cols = len(map), len(map[0])
    for row in range(rows):
        for col in range(cols):
            if map[row][col] == 'S':
                return True
    return False

def getRandomRadius(app, type):
    randomint = random.randint(10,20)
    if type == 'small':
        if randomint%2:
            app.smallRadius += 1
        else:
            app.smallRadius -= 1
    elif type == 'large':
        if randomint%2:
            app.largeRadius += 1
        else:
            app.largeRadius -= 1
    return
def drawBackGround(app):
    drawRect(0, 0, app.width, app.height, fill=gradient('silver', 'dimGray', start='center'))
    drawImage(app.bricks, 200, 130, width=200, height=200)
    drawImage(app.bricks, 1020, 450, width=200, height=200)
    drawImage(app.bricks, 700, 50, rotateAngle=180, width=200, height=200)
    width, height = getImageSize(app.torch)
    drawImage(app.torch, 150, 300)
    drawImage(app.torch, 1000, 300)
    smallRadius1, smallRadius2, bigRadius1, bigRadius2 = 10, 10, 10, 10

    if int(time.time()) % 2 == 0: 
        smallRadius1 = 12 + random.randint(0, 2)
        smallRadius2 = 15 + random.randint(0, 2)
        bigRadius1 = 28 -  random.randint(0, 2)
        bigRadius2 = 22 + random.randint(0, 2)
    elif int(time.time()) % 2 == 1:
        smallRadius1 = 20 - random.randint(0, 2)
        smallRadius2 = 13 + random.randint(0, 2)
        bigRadius1 = 25 +  random.randint(0, 2)
        bigRadius2 = 27 - random.randint(0, 2)
    drawCircle(150+width/2, 300-height/2+30, bigRadius1, fill='red')
    drawCircle(150+width/2, 300-height/2+30, smallRadius1, fill='yellow')
    drawCircle(1000+width/2, 300-height/2+30, bigRadius2, fill='red')
    drawCircle(1000+width/2, 300-height/2+30, smallRadius2, fill='yellow')
def drawTitlePage(app):
    drawBackGround(app)
    height, width = getImageSize(app.title)
    drawImage(app.title, app.width/2-width-85, app.height/2-200)

    #Play button
    buttonWidth = 200
    buttonHeight = 100
    playButton = Button(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2+150, app.width/2+buttonWidth/2, app.height/2+buttonHeight/2+150, 'Title Page', pressPlay, app.fillHover, app.fillNorm)
    checkHover(app, playButton)
    drawRect(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2+150, buttonWidth, buttonHeight, fill=playButton.getFill(), border=app.fillNorm)
    drawLabel('PLAY', app.width/2, app.height/2+150, fill=app.buttonTextFill)

    #Load button
def drawGameMenu(app):
    drawBackGround(app)

    drawLabel('SELECT A GAMEMODE:', app.width/2, app.height/2-200, fill='white', size=60)

    #Campaign button
    buttonWidth = 250
    buttonHeight = 300
    campaignButton = Button(app.width/2-buttonWidth-100, app.height/2-buttonHeight/2+100, app.width/2-100, app.height/2+buttonHeight/2+100,  'Game Menu', pressCampaign, app.fillHover, app.fillNorm)
    checkHover(app, campaignButton)
    drawRect(app.width/2-buttonWidth-100, app.height/2-buttonHeight/2+100, buttonWidth, buttonHeight, fill=campaignButton.getFill(), border=app.fillNorm )
    drawLabel('Play', app.width/2-buttonWidth/2-100, app.height/2+100, fill=app.buttonTextFill)

    #Map Editor button
    buttonWidth = 250
    buttonHeight = 300
    mapEditorButton = Button(app.width/2-buttonWidth+350, app.height/2-buttonHeight/2+100, app.width/2+350, app.height/2+buttonHeight/2+100, 'Game Menu', pressMapEditor, app.fillHover, app.fillNorm)
    checkHover(app, mapEditorButton)
    drawRect(app.width/2-buttonWidth+350, app.height/2-buttonHeight/2+100, buttonWidth, buttonHeight, fill=mapEditorButton.getFill(), border=app.fillNorm)
    drawLabel('Map Editor', app.width/2-buttonWidth/2+350, app.height/2+100, fill=app.buttonTextFill)
def drawCampaign(app):
    drawBackGround(app)
    buttonWidth = 200
    buttonHeight = 300

    tutorialButton = Button(app.width/2-buttonWidth/2-400, app.height/2-buttonHeight/2, app.width/2+buttonWidth/2-400, app.height/2+buttonHeight/2, 'Campaign', pressTutorial, app.fillHover, app.fillNorm)
    checkHover(app, tutorialButton)
    drawRect(app.width/2-buttonWidth/2-400, app.height/2-buttonHeight/2, buttonWidth, buttonHeight, fill=tutorialButton.getFill(), border=app.fillNorm)
    drawLabel('Tutorial', app.width/2-400, app.height/2, fill=app.buttonTextFill)

    endlessButton = Button(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2, app.width/2+buttonWidth/2, app.height/2+buttonHeight/2, 'Campaign', pressEndless, app.fillHover, app.fillNorm)
    checkHover(app, endlessButton)
    drawRect(app.width/2-buttonWidth/2, app.height/2-buttonHeight/2, buttonWidth, buttonHeight, fill=endlessButton.getFill(), border=app.fillNorm)
    drawLabel('Level 1', app.width/2, app.height/2, fill=app.buttonTextFill)
    
    loadButton = Button(app.width/2-buttonWidth/2+400, app.height/2-buttonHeight/2, app.width/2+buttonWidth/2+400, app.height/2+buttonHeight/2, 'Campaign', pressLoad, app.fillHover, app.fillNorm)
    checkHover(app, loadButton)
    drawRect(app.width/2-buttonWidth/2+400, app.height/2-buttonHeight/2, buttonWidth, buttonHeight, fill=loadButton.getFill(), border=app.fillNorm)
    drawLabel('Load a level', app.width/2+400, app.height/2, fill=app.buttonTextFill)
def drawMapEditor(app):
    drawMap(app)
    drawRect(1200, 0, 300, app.height, fill='brown')
    buttonWidth = 100
    buttonHeight = 100

    #Select 'end'
    if not findEnd(app, app.map):
        selectEndButton = Button(1350-buttonWidth/2, 100-buttonHeight/2, 1350+buttonWidth/2, 100+buttonHeight/2, 'Map Editor', pressSelectEndButton, app.fillHover, 'tan')
        checkHover(app, selectEndButton)
        drawRect(1350-buttonWidth/2, 100-buttonHeight/2, buttonWidth, buttonHeight, fill=selectEndButton.getFill(), border='tan')
        drawLabel('Select End', 1350, 100, fill=app.buttonTextFill)

    #Select 'Start'
    if not findStart(app, app.map):
        selectStartButton = Button(1350-buttonWidth/2, 100-buttonHeight/2, 1350+buttonWidth/2, 100+buttonHeight/2, 'Map Editor', pressSelectStartButton, app.fillHover, 'tan')
        checkHover(app, selectStartButton)
        drawRect(1350-buttonWidth/2, 100-buttonHeight/2, buttonWidth, buttonHeight, fill=selectStartButton.getFill(), border='tan')
        drawLabel('Select Start', 1350, 100, fill=app.buttonTextFill) 

    #select path
    selectPathButton = Button(1350-buttonWidth/2, 220-buttonHeight/2, 1350+buttonWidth/2, 220+buttonHeight/2, 'Map Editor', pressSelectPathButton, app.fillHover, 'tan')
    checkHover(app, selectPathButton)
    drawRect(1350-buttonWidth/2, 220-buttonHeight/2, buttonWidth, buttonHeight, fill=selectPathButton.getFill(), border='tan')
    drawLabel('Select Path', 1350, 220, fill=app.buttonTextFill)

    #select 1
    select1Button = Button(1350-buttonWidth/2, 340-buttonHeight/2, 1350+buttonWidth/2, 340+buttonHeight/2, 'Map Editor', pressSelect1Button, app.fillHover, 'lawnGreen')
    checkHover(app, select1Button)
    drawRect(1350-buttonWidth/2, 340-buttonHeight/2, buttonWidth, buttonHeight, fill=select1Button.getFill(), border='lawnGreen')
    drawLabel('Select Green', 1350, 340, fill='black')

    #select 0
    select0Button = Button(1350-buttonWidth/2, 460-buttonHeight/2, 1350+buttonWidth/2, 460+buttonHeight/2, 'Map Editor', pressSelect0Button, app.fillHover, 'limeGreen')
    checkHover(app, select0Button)
    drawRect(1350-buttonWidth/2, 460-buttonHeight/2, buttonWidth, buttonHeight, fill=select0Button.getFill(), border='limeGreen')
    drawLabel('Select Dark Green', 1350, 460, fill=app.buttonTextFill)

    #save
    saveButton = Button(1350-buttonWidth/2, 580-buttonHeight/2, 1350+buttonWidth/2, 580+buttonHeight/2, 'Map Editor', pressSaveButton, app.fillHover, app.fillNorm)
    checkHover(app, saveButton)
    drawRect(1350-buttonWidth/2, 580-buttonHeight/2, buttonWidth, buttonHeight, fill=saveButton.getFill(), border=app.fillNorm)
    drawLabel('Save Map', 1350, 580, fill=app.buttonTextFill)

def drawLoadMenu(app):
    drawBackGround(app)

    #Load Slot 1 button
    buttonWidth = 250
    buttonHeight = 300
    load1Button = Button(app.width/2-buttonWidth-100, app.height/2-buttonHeight/2+100, app.width/2-100, app.height/2+buttonHeight/2+100, 'Load Menu', pressLoad1, app.fillHover, app.fillNorm)
    checkHover(app, load1Button)
    drawRect(app.width/2-buttonWidth-100, app.height/2-buttonHeight/2+100, buttonWidth, buttonHeight, fill=load1Button.getFill(), border=app.fillNorm )
    drawLabel('Load Slot 1', app.width/2-buttonWidth/2-100, app.height/2+100, fill=app.buttonTextFill)

    #Load Slot 2 button
    buttonWidth = 250
    buttonHeight = 300
    load2Button = Button(app.width/2-buttonWidth+350, app.height/2-buttonHeight/2+100, app.width/2+350, app.height/2+buttonHeight/2, 'Load Menu', pressLoad2, app.fillHover, app.fillNorm)
    checkHover(app, load2Button)
    drawRect(app.width/2-buttonWidth+350, app.height/2-buttonHeight/2+100, buttonWidth, buttonHeight, fill=load2Button.getFill(), border=app.fillNorm)
    drawLabel('Load Slot 2', app.width/2-buttonWidth/2+350, app.height/2+100, fill=app.buttonTextFill)
    
def drawLoad(app):
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
        startWave = Button(app.startCell[0]*app.cellSize, app.startCell[1]*app.cellSize, app.startCell[0]*app.cellSize+app.cellSize, app.startCell[1]*app.cellSize+app.cellSize, 'Load', pressStartWave, 'crimson', 'fireBrick')
        checkHover(app, startWave)
        drawCircle(app.startCell[0]*app.cellSize + app.cellSize/2, app.startCell[1]*app.cellSize + app.cellSize/2, app.cellSize/3, fill=startWave.getFill(), border=startWave.fillNorm)
    
    #money
    drawCircle(25, 25, 20, fill='gold')
    drawCircle(25, 25, 15, fill='yellow')
    drawLabel(f'{app.money}', 75, 25, size=20)

    #heart
    drawImage(app.heart, 0, 50, width=50, height=50)
    drawLabel(f'{app.health}', 75, 75, size=20)

    if app.paused: drawPauseMenu(app, 'Load')

    #draw side menu
    if not app.paused:
        if app.placingTowers and not mouseInSideMenu(app): drawSideMenu(app)
        #previews
        if app.placement == 'm' and app.placingTowers: drawMagicPreview(app)
        elif app.placement == 'b' and app.placingTowers: drawBombPreview(app)
        elif app.placement == 'a' and app.placingTowers: drawArcherPreview(app)

        #need more money label
        #if app.needMoreMoneyDraw and app.placingTowers: drawLabel('NEED MORE MONEY!', app.mouseLocation[0], app.mouseLocation[1]-50, size=20)
        
        #upgrade tower menu
        if app.drawTowerUpgrade[0]: drawTowerUpgrade(app)

        #game over
        if app.gameOver: drawGameOver(app)

        if app.win: drawWin(app)
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

    if app.paused: drawPauseMenu(app, 'Endless')

    #draw side menu
    if not app.paused:
        if app.placingTowers and not mouseInSideMenu(app): drawSideMenu(app)
        #previews
        if app.placement == 'm' and app.placingTowers: drawMagicPreview(app)
        elif app.placement == 'b' and app.placingTowers: drawBombPreview(app)
        elif app.placement == 'a' and app.placingTowers: drawArcherPreview(app)

        #need more money label
        #if app.needMoreMoneyDraw and app.placingTowers: drawLabel('NEED MORE MONEY!', app.mouseLocation[0], app.mouseLocation[1]-50, size=20)
        
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

    if app.paused: drawPauseMenu(app, 'Tutorial')

    #draw side menu
    if not app.paused:
        if app.placingTowers and not mouseInSideMenu(app): drawSideMenu(app)
        #previews
        if app.placement == 'm' and app.placingTowers: drawMagicPreview(app)
        elif app.placement == 'b' and app.placingTowers: drawBombPreview(app)
        elif app.placement == 'a' and app.placingTowers: drawArcherPreview(app)

        #need more money label
        #if app.needMoreMoneyDraw and app.placingTowers: drawLabel('NEED MORE MONEY!', app.mouseLocation[0], app.mouseLocation[1]-50, size=20)
        
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
        drawLabel(f'Welcome to {app.titleName}!', app.width/2, app.height/2-gap*5, size=50, fill=fillColor)
        drawLabel(f'{app.titleName} is a tower defense game!', app.width/2, app.height/2+0*gap, size=30, fill=fillColor)
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
        drawLabel('S', location[0]+app.cellSize/2, location[1]+app.cellSize/2, fill='white')
    elif cell == 'E':
        drawRect(location[0], location[1], app.cellSize, app.cellSize, fill='tan')
        drawLabel('E', location[0]+app.cellSize/2, location[1]+app.cellSize/2, fill='white')
    elif cell == 'P':
        drawRect(location[0], location[1], app.cellSize, app.cellSize, fill='tan')
    elif cell == 0:
        drawRect(location[0], location[1], app.cellSize, app.cellSize, fill='limeGreen')
    elif cell == 1:
        drawRect(location[0], location[1], app.cellSize, app.cellSize, fill='lawnGreen')
    elif cell == None:
        drawRect(location[0], location[1], app.cellSize, app.cellSize, fill='white', border='black')

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
    drawLabel('280 coin', 1100, 200)

    #draw bomb tower
    drawLabel('Press "b" for Bomb', 1100, 300, size=16)
    drawCircle(1100, 350, BOMB_SIZE, fill='gray', opacity=100)
    drawLabel('320 coin', 1100, 350)

    #draw archer tower
    drawLabel('Press "a" for Archer', 1100, 450, size=16)
    drawCircle(1100, 500, ARCHER_SIZE, fill='brown', opacity=100)
    drawLabel('200 coin', 1100, 500)

def drawTowerUpgrade(app):
    pass
def drawGameOver(app):
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
        elif app.scene == "Map Editor" and app.loaded: drawMapEditor(app)
        elif app.scene == 'Endless' and app.loaded: drawEndless(app)
        elif app.scene == 'Tutorial' and app.loaded: drawTutorial(app)
        elif app.scene == 'Load' and app.loaded: drawLoad(app)

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
    print('pressed load')
def pressLoad1(app):
    f = open('save1.txt', 'r')
    map = f.read()
    app.map = parseMap(map)
    f.close()
    app.scene = 'Load'
    app.loaded = False
def pressLoad2(app):
    f = open('save2.txt', 'r')
    map = f.read()
    app.map = parseMap(map)
    f.close()
    app.scene = 'Load'
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
        app.showMessage('Play the tutorial first!')
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
def pressTutorial(app):
    app.scene = 'Tutorial'
    app.loaded = False
    print('current scene: Tutorial')
def pressBack(app):
    if app.scene == 'Game Menu': app.scene = 'Title Page'
    elif app.scene == 'Map Editor': app.scene = 'Game Menu'
    elif app.scene == 'Campaign': app.scene = 'Game Menu'
def pressSelectStartButton(app):
    app.selectedBlock = 'S'
def pressSelectEndButton(app):
    app.selectedBlock = 'E'
def pressSelectPathButton(app):
    app.selectedBlock = 'P'
def pressSelect0Button(app):
    app.selectedBlock = 0
def pressSelect1Button(app):
    app.selectedBlock = 1
def pressSaveButton(app):
    loadMap(app)
    if hasLegalPath(app):
        saveLocation = askSaveLocation(app)
        saveMap = copy.deepcopy(app.map)
        convertMap(saveMap)
        if saveLocation == '1':
            f = open(app.save1, 'w')
            f.write(str(saveMap))
            f.close()
        elif saveLocation == '2':
            f = open(app.save2, 'w')
            f.write(str(saveMap))
            f.close()
    else:
        app.showMessage('No legal enemy path or multiple paths')
        
#end button functions
def parseMap(map): #TAKEN FROM https://github.com/vixu8/hack112, main.py, lines 473 to 484, hack112 project
    returnMap = []
    map = map.strip('[[')
    map = map.strip(']]')
    listComas = map.split('], [')
    for comad in listComas:
        addList = []
        for c in comad:
            if c.isdigit():
                addList.append(int(c))
            elif c.isalpha():
                addList.append(c)
        returnMap.append(addList)
    return returnMap


def askSaveLocation(app):
    response = app.getTextInput('Pick a location to save (1 or 2): ')
    if not response in ['1', '2']:
        app.showMessage('Please enter "1" or "2"!')
        return askSaveLocation(app)
    return response

def convertMap(map):
    rows, cols = len(map), len(map[0])
    for row in range(rows):
        for col in range(cols):
            if map[row][col] == None:
                map[row][col] = 1
def hasLegalPath(app):
    if (not findStart(app, app.map)) or (not findEnd(app, app.map)): return False
    start = app.startCell
    end = app.endCell
    return hasLegalPathHelper(app, start, [], None, app.map)

def hasLegalPathHelper(app, location, list, prevDirection, map):
    if map[location[1]][location[0]] == 'E':
        list.append(((location[0]*app.cellSize + app.cellSize/2, location[1]*app.cellSize + app.cellSize/2), prevDirection))
        return True
    else:
        left = (location[0]-1, location[1])
        right = (location[0]+1, location[1])
        up = (location[0], location[1]-1)
        down = (location[0], location[1]+1)
        
        if prevDirection != 'right' and isLegalCell(app, left) and (map[left[1]][left[0]] == 'P' or map[left[1]][left[0]] == 'E'): #check left
            list.append(((left[0]*app.cellSize + app.cellSize/2, left[1]*app.cellSize + app.cellSize/2), 'left'))
            return hasLegalPathHelper(app, left, list, 'left', map)
        elif prevDirection != 'left' and isLegalCell(app, right) and (map[right[1]][right[0]] == 'P' or map[right[1]][right[0]] == 'E'): #check right
            list.append(((right[0]*app.cellSize + app.cellSize/2, right[1]*app.cellSize + app.cellSize/2), 'right'))
            return hasLegalPathHelper(app, right, list, 'right', map)
        elif prevDirection != 'up' and isLegalCell(app, down) and (map[down[1]][down[0]] == 'P' or map[down[1]][down[0]] == 'E'): #check down
            list.append(((down[0]*app.cellSize + app.cellSize/2, down[1]*app.cellSize + app.cellSize/2), 'down'))
            return hasLegalPathHelper(app, down, list, 'down', map)
        elif prevDirection != 'down' and isLegalCell(app, up) and (map[up[1]][up[0]] == 'P' or map[up[1]][up[0]] == 'E'): #check up
            list.append(((up[0]*app.cellSize + app.cellSize/2, up[1]*app.cellSize + app.cellSize/2), 'up'))
            return hasLegalPathHelper(app, up, list, 'up', map)
        else:
            return False
        


def onKeyPress(app, keys):
    if 'escape' == keys:
        pressBack(app)
    if 'k' == keys:
        app.loaded = True
        app.scene = "Game Menu"
    if 'r' == keys:
        app.loaded = True
        app.scene = 'Title Page'
    if app.scene in app.levels:
        if app.placingTowers:
            if 'm' == keys: app.placement = 'm'
            elif 'a' == keys: app.placement = 'a'
            elif 'b' == keys: app.placement = 'b'
        if 's' == keys:
            app.showingRange = True
        if 'p' == keys:
            app.paused = not app.paused

def onKeyRelease(app, keys):
    if app.scene in app.levels:
        if 's' in keys:
            app.showingRange = False

def onMouseDrag(app, mouseX, mouseY):
    if app.scene == 'Map Editor' and app.loaded:
        cellLocation = getCellLocation(app, (mouseX, mouseY))
        if (0 <= cellLocation[0] < 30) and (0 <= cellLocation[1] < 20):
            app.map[cellLocation[1]][cellLocation[0]] = app.selectedBlock

def onMouseMove(app, mouseX, mouseY):
    app.mouseLocation = (mouseX, mouseY)

def onMousePress(app, mouseX, mouseY):
    if app.scene == 'Map Editor' and app.loaded:
        cellLocation = getCellLocation(app, (mouseX, mouseY))
        if (0 <= cellLocation[0] < 30) and (0 <= cellLocation[1] < 20):
            app.map[cellLocation[1]][cellLocation[0]] = app.selectedBlock

    if app.scene == 'Tutorial':
        for i in range(len(app.checkpoints)):
            if not app.checkpoints[i]:
                app.checkpoints[i] = True
                if app.paused: 
                    app.paused = False
                return

    #check buttons
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
def getCellLocation(app, position):
    location = (position[0]//app.cellSize, position[1]//app.cellSize)
    return location
def intersectingCircles(position1, position2, size1, size2):
    return distance(position1[0], position1[1], position2[0], position2[1]) <= (size1 + size2)
def clickedTower(tower, position):
    towerPosition = tower.getPosition()
    towerSize = tower.getSize()
    return (towerPosition[0] - towerSize <= position[0] <= towerPosition[0] + towerSize) and (towerPosition[1] - towerSize <= position[1] <= towerPosition[1] + towerSize)

def main():
    runApp()

main()