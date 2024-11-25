from tower import *
import time

class Enemy:
    health = {'Goblin':100}
    parmor = {'Goblin':0}
    marmor = {'Goblin':0}

    def __init__(self, type, position) -> None:
        self.type = type
        self.position = position
        self.health = Enemy.health[type]
        self.parmor = Enemy.parmor[type]
        self.marmor = Enemy.marmor[type]
    
    def takeDamage(self, mdmg, pdmg):
        mdmgTaken = mdmg - self.marmor
        pdmgTaken = pdmg - self.parmor
        self.health = self.health - mdmgTaken - pdmgTaken
    

    