import os
import pygame
import math
from pygame.math import Vector2
from gamestate import GameState
from layer import ArrayLayer, UnitsLayer, BulletsLayer, ExplosionsLayer
from command import MoveCommand, TargetCommand, ShootCommand, MoveBulletCommand, DeleteDestroyedCommand

os.environ['SDL_VIDEO_CENTERED'] = '1'

class UserInterface:
    def __init__(self):
        pygame.init()
        self.game_state = GameState()

        self.cell_size = pygame.math.Vector2(64,64)

        self.layers = [
            ArrayLayer(self, "ground.png", self.game_state, self.game_state.ground),
            ArrayLayer(self, "walls.png", self.game_state, self.game_state.walls),
            UnitsLayer(self, "units.png", self.game_state, self.game_state.units),
            BulletsLayer(self, "explosions.png", self.game_state, self.game_state.bullets),
            ExplosionsLayer(self, "explosions.png")
        ]

        for layer in self.layers:
            self.game_state.add_observer(layer)

        self.commands = []
        self.player_unit = self.game_state.units[0]
        
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
        move_vector = Vector2()
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    move_vector.x = 1
                elif event.key == pygame.K_LEFT:
                    move_vector.x = -1
                elif event.key == pygame.K_DOWN:
                    move_vector.y = 1
                elif event.key == pygame.K_UP:
                    move_vector.y = -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True

        if (move_vector.x != 0 or move_vector.y != 0) and (self.player_unit.status != "destroyed"):
            command = MoveCommand(self.game_state, self.player_unit, move_vector)
            self.commands.append(command)
        
        mouse_pos = pygame.mouse.get_pos()
        target_cell = Vector2()
        target_cell.x = mouse_pos[0] / self.cell_width - 0.5
        target_cell.y = mouse_pos[1] / self.cell_height - 0.5
        command = TargetCommand(self.game_state, self.player_unit, target_cell)
        self.commands.append(command)

        for unit in self.game_state.units:
            if unit != self.player_unit:
                command = TargetCommand(self.game_state, unit, self.player_unit.position)
                self.commands.append(command)
                # create shoot command if player too close
                distance = unit.position.distance_to(self.player_unit.position)
                if distance <= self.game_state.bullet_range:
                    self.commands.append(ShootCommand(self.game_state, unit))
        
        if mouse_clicked:
            self.commands.append(ShootCommand(self.game_state, self.player_unit))

        for bullet in self.game_state.bullets:
            self.commands.append(MoveBulletCommand(self.game_state, bullet))

        self.commands.append(DeleteDestroyedCommand(self.game_state.bullets))

    def update(self):
        for command in self.commands:
            command.run()
        self.commands.clear()
        self.game_state.epoch += 1

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