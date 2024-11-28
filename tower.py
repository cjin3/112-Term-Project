from enemy import *
from projectile import *
import time
import random

#Magic tower constants
MAGIC_LVL0_COST = 280
MAGIC_LVL1_COST = 340
MAGIC_LVL2_COST = 540

MAGIC_LVL0_MDMG = (10, 20)
MAGIC_LVL1_MDMG = (30, 50)
MAGIC_LVL2_MDMG = (70, 100)

MAGIC_LVL0_RANGE = 100
MAGIC_LVL1_RANGE = 200
MAGIC_LVL2_RANGE = 300

MAGIC_LVL0_ATKSP = 2
MAGIC_LVL1_ATKSP = 7
MAGIC_LVL2_ATKSP = 7

#Archer tower constants
ARCHER_LVL0_COST = 200
ARCHER_LVL1_COST = 250
ARCHER_LVL2_COST = 340

ARCHER_LVL0_PDMG = (13, 15)
ARCHER_LVL1_PDMG = (34, 39)
ARCHER_LVL2_PDMG = (67, 75)

ARCHER_LVL0_RANGE = 100
ARCHER_LVL1_RANGE = 100
ARCHER_LVL2_RANGE = 100

ARCHER_LVL0_ATKSP = 4
ARCHER_LVL1_ATKSP = 3
ARCHER_LVL2_ATKSP = 3

#Bomb tower constants
BOMB_LVL0_COST = 320
BOMB_LVL1_COST = 440
BOMB_LVL2_COST = 600

BOMB_LVL0_PDMG = (15, 30)
BOMB_LVL1_PDMG = (27, 40)
BOMB_LVL2_PDMG = (50, 110)

BOMB_LVL0_RANGE = 50
BOMB_LVL1_RANGE = 50
BOMB_LVL2_RANGE = 50

BOMB_LVL0_ATKSP = 20
BOMB_LVL1_ATKSP = 18
BOMB_LVL2_ATKSP = 16

class Tower:
    def __init__(self, type, lvl, position):
        self.type = type
        self.lvl = lvl
        self.position = position
        self.pdmg = (0,0)
        self.mdmg = (0,0)
        self.attackSpeed = 1
        self.range = 30
        self.size = 30

        self.canAttack = True
        self.attackingEnemy = None
        self.time = time.time()
    
    def getLevel(self):
        return self.lvl
    def getType(self):
        return self.type
    def getRange(self):
        return self.range
    def getPosition(self):
        return self.position
    
    def upgrade(self):
        self.lvl += 1

    def dealDamage(self, enemy):
        pdmg = random.randint(self.pdmg[0], self.pdmg[1])
        mdmg = random.randint(self.mdmg[0], self.mdmg[1])
        self.canAttack = False
        self.attackingEnemy = enemy
        return (pdmg, mdmg)
    def checkAttack(self):
        currentTime = time.time()
        if currentTime - self.time >= self.attackSpeed: 
            self.canAttack = True
            self.time = currentTime
        
    
    def __eq__(self, other) -> bool:
        return (other.isinstance(Tower)) and (self.lvl == other.lvl) and (self.position == other.position) and (self.type == other.type)

class Magic(Tower):
    def __init__(self, type, position, lvl):
        super().__init__(type, lvl, position)
        self.pdmg = (0,0)
        if self.lvl == 0: 
            self.cost = MAGIC_LVL0_COST
            self.mdmg = MAGIC_LVL0_MDMG
            self.range = MAGIC_LVL0_RANGE
            self.attackSpeed = MAGIC_LVL0_ATKSP
        elif self.lvl == 1: 
            self.cost = MAGIC_LVL1_COST
            self.mdmg = MAGIC_LVL1_MDMG
            self.range = MAGIC_LVL1_RANGE
        elif self.lvl == 2: 
            self.cost = MAGIC_LVL2_COST
            self.mdmg = MAGIC_LVL2_MDMG
            self.range = MAGIC_LVL2_RANGE

class Archer(Tower):
    def __init__(self, type, position, lvl):
        super().__init__(type, lvl, position)
        if self.lvl == 0: self.cost = ARCHER_LVL0_COST
        elif self.lvl == 1: self.cost = ARCHER_LVL1_COST
        elif self.lvl == 2: self.cost = ARCHER_LVL2_COST

class Bomb(Tower):
    def __init__(self, type, position, lvl):
        super().__init__(type, lvl, position)
        if self.lvl == 0: self.cost = BOMB_LVL0_COST
        elif self.lvl == 1: self.cost = BOMB_LVL1_COST
        elif self.lvl == 2: self.cost = BOMB_LVL2_COST
