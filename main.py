from cmu_graphics import *
import time
import math
import random

def onAppStart(app):
    app.scenes = ['Title Page', 'Game Menu']

    restart(app)

def restart(app):
    app.scene = 'Title Page'

    #app functions

def loadTitlePage(app):
    app.width = 1200
    app.height = 800

def onStep(app):
    if not app.paused and not app.gameOver:
        takeStep(app)
                                                                               
def takeStep(app):
    #loading things
    if app.scene == 'Title Page':
        loadTitlePage(app)

def drawTitlePage(app):
    drawLabel("press h to enter a score", 200, 200, size=16)

def redrawAll(app):
    if app.scene == 'Title Page':
        drawTitlePage(app)

def onKeyPress(app, keys):
    pass
        
def main():
    runApp()

main()