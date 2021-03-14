import pygame
from pygame.math import Vector2
from unit import Tank, Tower

class GameState:
    world_size: pygame.math.Vector2
    tank_pos: pygame.math.Vector2

    def __init__(self):
        self.world_size = pygame.math.Vector2(16,10)
        self.tank_pos = pygame.math.Vector2(0,0)

        tower1_pos = pygame.math.Vector2(10,3)
        tower2_pos = pygame.math.Vector2(10,5)

        self.units = [
            Tank(self, pygame.Vector2(5,4), pygame.math.Vector2(1,0)),
            Tower(self, pygame.Vector2(10,3), pygame.math.Vector2(0,1)),
            Tower(self, pygame.Vector2(10,5), pygame.math.Vector2(0,1)),
        ]
        self.ground = [ 
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(6,4), Vector2(7,2), Vector2(7,2)],
            [ Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(6,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(6,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(7,1)],
            [ Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,5), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(7,2), Vector2(8,5), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(7,1)],
            [ Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(7,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(6,4), Vector2(7,2), Vector2(7,2), Vector2(8,4), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1)],
            [ Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(5,1), Vector2(5,1), Vector2(7,1), Vector2(5,1), Vector2(5,1), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(7,4), Vector2(7,2), Vector2(7,2)],
            [ Vector2(5,1), Vector2(5,1), Vector2(6,2), Vector2(6,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1), Vector2(5,1)]
        ]

        self.walls = [
            [ None, None, None, None, None, None, None, None, None, Vector2(1,3), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1)],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(1,3), Vector2(1,1), Vector2(0,3), None],
            [ None, None, None, None, None, None, None, Vector2(1,1), Vector2(1,1), Vector2(3,3), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, None, None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, Vector2(1,1), Vector2(1,1), Vector2(0,3), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(2,1), None, Vector2(2,1), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, Vector2(2,3), Vector2(1,1), Vector2(3,3), None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,1), None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None, None, Vector2(2,3), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1), Vector2(1,1)]
        ]
        
    @property
    def world_width(self):
        return int(self.world_size.x)

    @property
    def world_height(self): 
        return int(self.world_size.y)

    def update(self, move_tank_command: pygame.math.Vector2, target_command: Vector2):
        for unit in self.units:
            unit.move(move_tank_command)
        for unit in self.units:
            unit.orient_weapon(target_command)
