class Button:
    buttonLocations = {}
    buttonFunctions = {}

    def __init__(self, topLeftX, topLeftY, botRightX, botRightY, scene, func, fillHover, fillNorm):
        self.fillHover = fillHover
        self.fillNorm = fillNorm
        print(self.fillNorm, self.fillHover)
        self.fill = self.fillNorm
        self.topLeft = (topLeftX, topLeftY)
        self.botRight = (botRightX, botRightY)
        self.location = (self.topLeft, self.botRight, scene)
        self.func = func
        
        Button.buttonLocations[self.location] = self
        Button.buttonFunctions[self] = self.func
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, Button)) and (self.location == other.location) and (self.func == other.func)
    def __hash__(self):
        return hash((self.location, self.func))
    def __repr__(self):
        return f'<Button location={self.location}, func={self.func}, fill={self.fill}>'
    
    def setFillHover(self): 
        self.fill = self.fillHover
        print(self.fill, self.fillHover)
    def setFillNorm(self): self.fill = self.fillNorm

    def getLocation(self): return self.location
    def getFunc(self): return self.func
    def getFill(self): return self.fill