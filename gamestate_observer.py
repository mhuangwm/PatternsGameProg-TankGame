class GameStateObserver():
    def unitDestroyed(self,unit):
        pass

    def bulletFired(self, unit):
        pass

class GameModeObserver():
    def loadLevelRequested(self, fileName):
        pass

    def worldSizeChanged(self, worldSize):
        pass

    def showMenuRequested(self):
        pass

    def showGameRequested(self):
        pass

    def gameWon(self):
        pass

    def gameLost(self):
        pass

    def quitRequested(self):
        pass