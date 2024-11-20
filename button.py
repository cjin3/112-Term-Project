class Button:
    buttonLocations = {}
    buttonFunctions = {}

    def __init__(self, topLeftX, topLeftY, botRightX, botRightY, scene, func):
        self.topLeft = (topLeftX, topLeftY)
        self.botRight = (botRightX, botRightY)
        self.location = (self.topLeft, self.botRight, scene)
        self.func = func
        
        Button.buttonLocations[self.location] = self
        Button.buttonFunctions[self] = self.func
    
    def getLocation(self):
        return self.location
    def getFunc(self):
        return self.func