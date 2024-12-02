from enemy import *
from tower import *
import copy


class Projectile:
    PROJECTILE_SPEED_M = {0:4, 1:4, 2:5}
    PROJECTILE_SPEED_B = {0:1, 1:2, 2:2}
    PROJECTILE_SPEED_A = {0:3, 1:4, 2:5}

    PROJECTILE_SIZE_M = {0:3, 1:3, 2:3}
    PROJECTILE_SIZE_B = {0:7, 1:7, 2:8}
    PROJECTILE_SIZE_A = {0:2, 1:2, 2:3}

    PROJECTILE_COLOR_M = 'blue'
    PROJECTILE_COLOR_B = 'black'
    PROJECTILE_COLOR_A = 'brown'

    def __init__(self, Tower, Enemy, position, damage) -> None:
        self.Tower = Tower
        self.Enemy = Enemy
        self.position = position
        self.dmg = damage
        enemyDirection = Enemy.getPosition()
        self.direction = (enemyDirection[0]-position[0], enemyDirection[1]-position[1])
        self.direction = Projectile.normalize(self.direction)

        self.speed = 0
        self.size = 1
        self.color = 'white'
        towerType = self.Tower.getType()
        towerLvl = self.Tower.getLevel()
        if towerType == 'Magic': 
            self.speed = Projectile.PROJECTILE_SPEED_M[towerLvl]
            self.size = Projectile.PROJECTILE_SIZE_M[towerLvl]
            self.color = Projectile.PROJECTILE_COLOR_M
        elif towerType == 'Bomb': 
            self.speed = Projectile.PROJECTILE_SPEED_B[towerLvl]
            self.size = Projectile.PROJECTILE_SIZE_B[towerLvl]
            self.color = Projectile.PROJECTILE_COLOR_B
        elif towerType == 'Archer': 
            self.speed = Projectile.PROJECTILE_SPEED_A[towerLvl]
            self.size = Projectile.PROJECTILE_SIZE_A[towerLvl]
            self.color = Projectile.PROJECTILE_COLOR_A
    
    def move(self):
        self.position = (self.position[0] + self.direction[0]*self.speed, self.position[1] + self.direction[1]*self.speed)

    def getPosition(self): return self.position
    def getSize(self): return self.size
    def getColor(self): return self.color

    @staticmethod
    def normalize(vector):
        magnitude = (vector[0]**2 + vector[1]**2)**(1/2)
        return (vector[0]/magnitude, vector[1]/magnitude)

class MagicProjectile(Projectile):
    def __init__(self, Tower, Enemy, position, damage) -> None:
        super().__init__(Tower, Enemy, position, damage)

class ArcherProjectile(Projectile):
    def __init__(self, Tower, Enemy, position, damage) -> None:
        super().__init__(Tower, Enemy, position, damage)

class BombProjectile(Projectile):
    def __init__(self, Tower, Enemy, position, damage) -> None:
        super().__init__(Tower, Enemy, position, damage)