import os
import pygame
from pygame.math import Vector2

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Unit:
    def __init__(self, state, position, tile):
        self.state = state
        self.position = position
        self.tile = tile

    def move(self, move_vector):
        raise NotImplementedError()

class Tank(Unit):
    def move(self, move_vector):
        new_pos = self.position + move_vector

        # check world boundaries
        if new_pos.x < 0 or new_pos.x >= self.state.world_size.x\
        or new_pos.y < 0 or new_pos.y >= self.state.world_size.y:
            return
        
        # check unit collision
        for unit in self.state.units:
            if new_pos == unit.position:
                return

        self.position = new_pos

class Tower(Unit):
    def move(self, move_vector): pass

class GameState:
    world_size: pygame.math.Vector2
    tank_pos: pygame.math.Vector2

    @property
    def world_width(self):
        return int(self.world_size.x)

    @property
    def world_height(self): 
        return int(self.world_size.y)

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
        
    def update(self, move_tank_command: pygame.math.Vector2):
        for unit in self.units:
            unit.move(move_tank_command)

class UserInterface:
    @property
    def cell_width(self):
        return int(self.cell_size.x)

    @property
    def cell_height(self):
        return int(self.cell_size.y)

    def __init__(self):
        pygame.init()
        self.game_state = GameState()

        self.cell_size = pygame.math.Vector2(64,64)
        self.units_texture = pygame.image.load("units.png")
        self.grounds_texture = pygame.image.load("ground.png")
        
        window_size = self.game_state.world_size.elementwise() * self.cell_size
        self.window = pygame.display.set_mode(
            (int(window_size.x), int(window_size.y))
        )

        pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("icon.png"))

        self.move_tank_command = pygame.math.Vector2(0,0)
        self.clock = pygame.time.Clock()
        self.running = True

    def process_input(self):
        self.move_tank_command = pygame.math.Vector2(0,0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    self.move_tank_command.x = 1
                elif event.key == pygame.K_LEFT:
                    self.move_tank_command.x = -1
                elif event.key == pygame.K_DOWN:
                    self.move_tank_command.y = 1
                elif event.key == pygame.K_UP:
                    self.move_tank_command.y = -1

    def update(self):
        self.game_state.update(self.move_tank_command)

    def render_unit(self, unit: Unit):
        # location on screen:
        sprite_point = unit.position.elementwise() * self.cell_size
        
        # unit texture on tilemap
        texture_point = unit.tile.elementwise() * self.cell_size
        texture_rect = pygame.Rect(
            int(texture_point.x), int(texture_point.y),
            int(self.cell_width), int(self.cell_height)
        )
        self.window.blit(self.units_texture, sprite_point, texture_rect)

    def render_ground(self, position, tile):
        sprite_point = position.elementwise() * self.cell_size
        texture_point = tile.elementwise() * self.cell_size
        texture_rect = pygame.Rect(
            int(texture_point.x), int(texture_point.y),
            int(self.cell_width), int(self.cell_height)
        )
        self.window.blit(self.grounds_texture, sprite_point, texture_rect)

    def render(self):
        self.window.fill((0,0,0))
        for y in range (int(self.game_state.world_size.y)):
            for x in range(int(self.game_state.world_size.x)):
                self.render_ground(pygame.math.Vector2(x,y), self.game_state.ground[y][x])

        for unit in self.game_state.units:
            self.render_unit(unit)

        pygame.display.update()

    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(60)

user_interface = UserInterface()
user_interface.run()
pygame.quit()