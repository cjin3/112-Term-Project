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

    def __init__(self, type, position, startCell, enemyPath) -> None:
        self.type = type
        self.position = position
        self.health = Enemy.health[type]
        self.parmor = Enemy.parmor[type]
        self.marmor = Enemy.marmor[type]
        self.size = Enemy.size[type]
        self.speed = Enemy.speed[type]
        self.prevCell = startCell
        firstSpot = enemyPath[0]
        self.nextCell = firstSpot[0]
        print(self.position, self.prevCell, self.nextCell)
        self.instance = Enemy.instance.get(type, 0) + 1
        Enemy.instance[self.type] = self.instance

    def __eq__(self, other) -> bool:
        return (isinstance(other, Enemy)) and (self.type == other.type) and (self.instance == other.instance)

    def move(self, path):
        #find where enemy currently is
        #go to the next one
        #[((60.0, 380.0), 'right'), ((100.0, 380.0), 'right'), ((100.0, 420.0), 'down'), ((140.0, 420.0), 'right'), 
        # ((180.0, 420.0), 'right'), ((180.0, 380.0), 'up'), ((220.0, 380.0), 'right'), ((260.0, 380.0), 'right'), 
        # ((300.0, 380.0), 'right'), ((340.0, 380.0), 'right'), ((380.0, 380.0), 'right'), ((420.0, 380.0), 'right'), 
        # ((460.0, 380.0), 'right'), ((500.0, 380.0), 'right'), ((540.0, 380.0), 'right'), ((580.0, 380.0), 'right'), 
        # ((620.0, 380.0), 'right'), ((660.0, 380.0), 'right'), ((700.0, 380.0), 'right'), ((740.0, 380.0), 'right'), 
        # ((780.0, 380.0), 'right'), ((820.0, 380.0), 'right'), ((860.0, 380.0), 'right'), ((900.0, 380.0), 'right'), 
        # ((940.0, 380.0), 'right'), ((980.0, 380.0), 'right'), ((1020.0, 380.0), 'right'), ((1060.0, 380.0), 'right'), 
        # ((1100.0, 380.0), 'right'), ((1140.0, 380.0), 'right'), ((1180.0, 380.0), 'right'), ((1180.0, 380.0), 'right')]
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
        print(self.position, self.prevCell, self.nextCell, direction)



    def takeDamage(self, pdmg, mdmg):
        mdmgTaken = mdmg - self.marmor
        pdmgTaken = pdmg - self.parmor
        self.health = self.health - mdmgTaken - pdmgTaken
    
    def getHealth(self): return self.health
    def getPosition(self): return self.position
    def getType(self): return self.type
    

    