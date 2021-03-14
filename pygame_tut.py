import os
import pygame
import math
from pygame.math import Vector2
from gamestate import GameState
from layer import ArrayLayer, UnitsLayer

os.environ['SDL_VIDEO_CENTERED'] = '1'

class UserInterface:
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
        self.target_command = Vector2(0,0)
        self.clock = pygame.time.Clock()
        self.running = True

    @property
    def cell_width(self):
        return int(self.cell_size.x)

    @property
    def cell_height(self):
        return int(self.cell_size.y)


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

        mouse_pos = pygame.mouse.get_pos()
        self.target_command.x = mouse_pos[0] / self.cell_width - 0.5
        self.target_command.y = mouse_pos[1] / self.cell_height - 0.5

    def update(self):
        self.game_state.update(self.move_tank_command, self.target_command)

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

user_interface = UserInterface()
user_interface.run()
pygame.quit()