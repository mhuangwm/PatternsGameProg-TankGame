from pygame.math import Vector2

class GameItem:
    def __init__(self, state, position, tile):
        self.state = state
        self.status = "alive"
        self.position = position
        self.tile = tile
        self.orientation = 0

class Unit(GameItem):
    def __init__(self, state, position, tile):
        super().__init__(state,position,tile)
        self.weapon_target = Vector2(0,0)
        self.last_bullet_epoch = -100

class Bullet(GameItem):
    def __init__(self, state, unit):
        super().__init__(state, unit.position, Vector2(2,1))
        self.unit = unit
        self.start_position = unit.position
        self.end_position = unit.weapon_target