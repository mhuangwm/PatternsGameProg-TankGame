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

        self.layers = [
            ArrayLayer(self, "ground.png", self.game_state, self.game_state.ground),
            ArrayLayer(self, "walls.png", self.game_state, self.game_state.walls),
            UnitsLayer(self, "units.png", self.game_state, self.game_state.units)
        ]
        
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

    def render(self):
        self.window.fill((0,0,0))
        for layer in self.layers:
            layer.render(self.window)

        pygame.display.update()

    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(60)

class Layer:
    def __init__(self, ui, image_file):
        self.ui = ui
        self.texture = pygame.image.load(image_file)

    def render_tile(self, surface, position, tile):
        sprite_point = position.elementwise() * self.ui.cell_size

        # location of texture
        texture_point = tile.elementwise() * self.ui.cell_size

        # create rectangle to contain texture
        tecture_rect = pygame.Rect(
            int(texture_point.x), int(texture_point.y),
            int(self.ui.cell_width), int(self.ui.cell_height)
        )

        # blit the texture onto the surface
        surface.blit(self.texture, sprite_point, tecture_rect)

    def render(self, surface):
        raise NotImplementedError()

class ArrayLayer(Layer):
    def __init__(self, ui, image_file, game_state, array):
        super().__init__(ui, image_file)
        self.game_state = game_state
        self.array = array

    def render(self, surface):
        for y in range(self.game_state.world_height):
            for x in range(self.game_state.world_width):
                tile = self.array[y][x]
                if not tile is None:
                    self.render_tile(surface, Vector2(x,y), tile)

class UnitsLayer(Layer):
    def __init__(self, ui, image_file, game_state, units):
        super().__init__(ui, image_file)
        self.game_state = game_state
        self.units = units

    def render(self, surface):
        for unit in self.units:
            self.render_tile(surface, unit.position, unit.tile)
            self.render_tile(surface, unit.position, Vector2(0, 6))

user_interface = UserInterface()
user_interface.run()
pygame.quit()