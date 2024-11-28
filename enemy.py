from tower import *
from projectile import *
import time

class Enemy:
    instance = {}
    health = {'Goblin':100}
    parmor = {'Goblin':0}
    marmor = {'Goblin':0}
    size = {'Goblin':10}

    def __init__(self, type, position) -> None:
        self.type = type
        self.position = position
        self.health = Enemy.health[type]
        self.parmor = Enemy.parmor[type]
        self.marmor = Enemy.marmor[type]
        self.size = Enemy.size[type]
        self.instance = Enemy.instance.get(type, 0) + 1
        Enemy.instance[self.type] = self.instance

    
    def __eq__(self, other) -> bool:
        return (isinstance(other, Enemy)) and (self.type == other.type) and (self.instance == other.instance)

    def takeDamage(self, pdmg, mdmg):
        mdmgTaken = mdmg - self.marmor
        pdmgTaken = pdmg - self.parmor
        self.health = self.health - mdmgTaken - pdmgTaken
    def getHealth(self):
        return self.health
    def getPosition(self):
        return self.position
    

    