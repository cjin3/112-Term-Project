from tower import *
from projectile import *
import time

cellSize = 40

class Enemy:
    instance = {}
    health = {'Goblin':100}
    parmor = {'Goblin':0}
    marmor = {'Goblin':0}
    size = {'Goblin':10}
    speed = {'Goblin':1}
    money = {'Goblin':40}
    healthLost = {'Goblin':1}

    def __init__(self, type, position, startCell, enemyPath) -> None:
        self.type = type
        self.position = position
        self.health = Enemy.health[type]
        self.parmor = Enemy.parmor[type]
        self.marmor = Enemy.marmor[type]
        self.size = Enemy.size[type]
        self.speed = Enemy.speed[type]
        self.money = Enemy.money[type]
        self.healthLost = Enemy.healthLost[type]
        self.prevCell = startCell
        firstSpot = enemyPath[0]
        self.nextCell = firstSpot[0]
        self.finalCell = enemyPath[-1][0]
        self.reachedEnd = False
        self.instance = Enemy.instance.get(type, 0) + 1
        Enemy.instance[self.type] = self.instance

    def __eq__(self, other) -> bool:
        return (isinstance(other, Enemy)) and (self.type == other.type) and (self.instance == other.instance)

    def move(self, path):
        for i in range(len(path)-1):
            spot = path[i]
            nextSpot = path[i+1]
            direction = path[i][1]
            if spot[0] == self.nextCell:
                directVector = (0,0)
                if direction == 'left': directVector = (-1, 0)
                elif direction == 'right': directVector = (1, 0)
                elif direction == 'up': directVector = (0, -1)
                elif direction == 'down': directVector = (0, 1)
                self.position = (self.position[0] + directVector[0] * self.speed, self.position[1] + directVector[1] * self.speed)
                newNextSpot = nextSpot
                spot = path[i]
                newDirection = spot[1]
        if self.position[0] >= self.nextCell[0] and newDirection == 'right':
            self.position = (self.nextCell[0], self.position[1])
            self.prevCell = self.nextCell
            self.nextCell = newNextSpot[0]
        elif self.position[0] <= self.nextCell[0] and newDirection == 'left':
            self.position = (self.nextCell[0], self.position[1])
            self.prevCell = self.nextCell
            self.nextCell = newNextSpot[0]
        elif self.position[1] >= self.nextCell[1] and newDirection == 'down':
            self.position = (self.position[0], self.nextCell[1])
            self.prevCell = self.nextCell
            self.nextCell = newNextSpot[0]
        elif self.position[1] <= self.nextCell[1] and newDirection == 'up':
            self.position = (self.position[0], self.nextCell[1])
            self.prevCell = self.nextCell
            self.nextCell = newNextSpot[0]
        if self.finalCell == self.prevCell:
            self.reachedEnd = True



    def takeDamage(self, pdmg, mdmg):
        mdmgTaken = mdmg - self.marmor
        pdmgTaken = pdmg - self.parmor
        self.health = self.health - mdmgTaken - pdmgTaken
    
    def getHealth(self): return self.health
    def getPosition(self): return self.position
    def getType(self): return self.type
    def getFinished(self): return self.reachedEnd
    def getMoney(self): return self.money
    def getHealthLost(self): return self.healthLost
    

    