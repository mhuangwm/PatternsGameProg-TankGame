from pygame.math import Vector2

class GameItem():
    def __init__(self,state,position,tile):
        self.state = state
        self.status = "alive"
        self.position = position
        self.tile = tile
        self.orientation = 0    
    
class Unit(GameItem):
    def __init__(self,state,position,tile):
        super().__init__(state,position,tile)
        self.weaponTarget = Vector2(0,0)
        self.lastBulletEpoch = -100
        
class Bullet(GameItem):
    def __init__(self,state,unit):
        super().__init__(state,unit.position,Vector2(2,1))
        self.unit = unit
        self.startPosition = unit.position
        self.endPosition = unit.weaponTarget