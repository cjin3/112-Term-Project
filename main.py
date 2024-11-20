from cmu_graphics import *
import time
import math
import random

from button import *
from enemy import *
from tower import *

def onAppStart(app):
    app.scenes = ['Title Page', 'Game Menu']
    app.loadingDict = {'Title Page': loadTitlePage, 'Game Menu': loadGameMenu}

    restart(app)

def restart(app):
    app.prevScene = 'Title Page'
    app.scene = 'Title Page'
    app.paused = False
    app.gameOver = False

    #app functions

def loadTitlePage(app):
    app.width = 1200
    app.height = 800
def loadGameMenu(app):
    app.width = 100
    app.height = 300


def onStep(app):
    checkChangeScene(app)
    if not app.paused and not app.gameOver:
        takeStep(app)

def checkChangeScene(app):
    if app.scene != app.prevScene:
        app.prevScene = app.scene
        app.loadingDict[app.scene](app)

def takeStep(app):
    #loading things
    #if app.scene == 'Title Page':
        #loadTitlePage(app)
    pass

def drawTitlePage(app):
    drawLabel("TITLE", app.width/2, app.height/2, size=16)

def redrawAll(app):
    if app.scene == 'Title Page':
        drawTitlePage(app)

def onKeyPress(app, keys):
    if 'k' in keys:
        app.scene = "Game Menu"

def onMousePress(app, mouseX, mouseY):
    #check buttons
    for location in Button.buttonLocations.keys():
        if (app.scene == location[2]) and (location[0][0] <= mouseX <= location[1][0]) and (location[0][1] <= mouseY <= location[1][1]): #clicked button
            clicked = Button.buttonLocations[location]
            Button.buttonFunctions[clicked](app)
            

        
def main():
    runApp()

main()