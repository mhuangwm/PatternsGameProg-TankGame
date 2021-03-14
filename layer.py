import math
import pygame
from pygame.math import Vector2

class Layer:
    def __init__(self, ui, image_file):
        self.ui = ui
        self.texture = pygame.image.load(image_file)

    def render_tile(self, surface, position, tile, angle=None):
        sprite_point = position.elementwise() * self.ui.cell_size

        # location of texture
        texture_point = tile.elementwise() * self.ui.cell_size

        # create rectangle to contain texture
        tecture_rect = pygame.Rect(
            int(texture_point.x), int(texture_point.y),
            int(self.ui.cell_width), int(self.ui.cell_height)
        )

        # blit the texture onto the surface
        if angle is None:
            surface.blit(self.texture, sprite_point, tecture_rect)
        else:
            texture_tile = pygame.surface.Surface(
                (self.ui.cell_width, self.ui.cell_height), pygame.SRCALPHA
            )
            texture_tile.blit(self.texture, (0,0), tecture_rect)
            rotated_tile = pygame.transform.rotate(texture_tile, angle)
            # calculated new sprite point after rotation
            sprite_point.x -= (rotated_tile.get_width() - texture_tile.get_width()) // 2
            sprite_point.y -= (rotated_tile.get_height() - texture_tile.get_height()) // 2

            surface.blit(rotated_tile, sprite_point)


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
            size = unit.weapon_target - unit.position
            angle = math.atan2(-size.x, -size.y) * 180 / math.pi
            self.render_tile(surface, unit.position, Vector2(0, 6), angle)
