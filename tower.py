from enemy import *
import time
import random

#Magic tower costs
MAGIC_LVL0_COST = 280
MAGIC_LVL1_COST = 340
MAGIC_LVL2_COST = 540

#Archer tower costs
ARCHER_LVL0_COST = 200
ARCHER_LVL1_COST = 250
ARCHER_LVL2_COST = 340

#Bomb tower costs
BOMB_LVL0_COST = 320
BOMB_LVL1_COST = 440
BOMB_LVL2_COST = 600

#Magic tower dmg
MAGIC_LVL0_MDMG = (10, 20)
MAGIC_LVL1_MDMG = (30, 50)
MAGIC_LVL2_MDMG = (70, 100)

#Archer tower dmg
ARCHER_LVL0_PDMG = (13, 15)
ARCHER_LVL1_PDMG = (34, 39)
ARCHER_LVL2_PDMG = (67, 75)

#Bomb tower dmg
BOMB_LVL0_PDMG = (15, 30)
BOMB_LVL1_PDMG = (27, 40)
BOMB_LVL2_PDMG = (50, 110)

#

class Tower:
    def __init__(self, type, lvl):
        self.type = type
        self.lvl = lvl
    
    def getLevel(self):
        return self.lvl
    def getType(self):
        return self.type
    def upgrade(self):
        self.lvl += 1

class Wizard(Tower):
    def __init__(self, type, lvl):
        super().__init__(type, lvl)
        self.pdmg = (0,0)
        if self.lvl == 0: 
            self.cost = MAGIC_LVL0_COST
            self.mdmg = MAGIC_LVL0_MDMG
        elif self.lvl == 1: 
            self.cost = MAGIC_LVL1_COST
            self.mdmg = MAGIC_LVL1_MDMG
        elif self.lvl == 2: 
            self.cost = MAGIC_LVL2_COST
            self.mdmg = MAGIC_LVL2_MDMG

class Archer(Tower):
    def __init__(self, type, lvl):
        super().__init__(type, lvl)
        if self.lvl == 0: self.cost = ARCHER_LVL0_COST
        elif self.lvl == 1: self.cost = ARCHER_LVL1_COST
        elif self.lvl == 2: self.cost = ARCHER_LVL2_COST

class Bomb(Tower):
    def __init__(self, type, lvl):
        super().__init__(type, lvl)
        if self.lvl == 0: self.cost = BOMB_LVL0_COST
        elif self.lvl == 1: self.cost = BOMB_LVL1_COST
        elif self.lvl == 2: self.cost = BOMB_LVL2_COST
