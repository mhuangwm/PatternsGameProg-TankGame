from pygame.math import Vector2
from unit import Bullet

class Command:
    def run(self):
        raise NotImplementedError()

class MoveCommand(Command):
    def __init__(self, state, unit, move_vector):
        self.state = state
        self.unit = unit
        self.move_vector = move_vector

    def run(self):
        # update unit orientation 
        if self.move_vector.x < 0:
            self.unit.orientation = 90
        elif self.move_vector.x > 0:
            self.unit.orientation = -90
        if self.move_vector.y < 0:
            self.unit.orientation = 0
        elif self.move_vector.y > 0:
            self.unit.orientation = 180

        # compute new tank position
        new_pos = self.unit.position + self.move_vector

        # check world boundaries
        if new_pos.x < 0 or new_pos.x >= self.state.world_size.x\
        or new_pos.y < 0 or new_pos.y >= self.state.world_size.y:
            return
        
        # don't allow wall positions
        if not self.state.walls[int(new_pos.y)][int(new_pos.x)] is None:
            return
        
        # check unit collision
        for other_unit in self.state.units:
            if new_pos == other_unit.position:
                return

        self.unit.position = new_pos
        

class TargetCommand(Command):
    def __init__(self, state, unit, target):
        self.state = state
        self.unit = unit
        self.target = target
    
    def run(self):
        self.unit.weapon_target = self.target

class ShootCommand(Command):
    def __init__(self, state, unit):
        self.state = state
        self.unit = unit

    def run(self):
        if self.unit.status != "alive":
            return
        if self.state.epoch - self.unit.last_bullet_epoch\
        < self.state.bullet_delay:
            return

        self.unit.last_bullet_epoch = self.state.epoch
        self.state.bullets.append(Bullet(self.state, self.unit))

class MoveBulletCommand(Command):
    def __init__(self, state, bullet):
        self.state = state
        self.bullet = bullet

    def run(self):
        direction = (self.bullet.end_position - self.bullet.start_position).normalize()
        new_pos = self.bullet.position + self.state.bullet_speed * direction
        new_center_pos = new_pos + Vector2(0.5,0.5)

        # if bullet goes outside the world, destroy it
        if not self.state.is_inside(new_pos):
            self.bullet.status = "destroyed"
            return

        # if bullet goes towards the target cell, destroy it
        if ((direction.x > 0 and new_pos.x >= self.bullet.end_position.x) \
        or (direction.x < 0 and new_pos.x <= self.bullet.end_position.x)) \
        and ((direction.y >= 0 and new_pos.y >= self.bullet.end_position.y) \
        or (direction.y < 0 and new_pos.y <= self.bullet.end_position.y)):
            self.bullet.status = "destroyed"
            return

        # if bullet is outside of allowed rangem destroy it:
        if new_pos.distance_to(self.bullet.start_position) >= self.state.bullet_range:
            self.bullet.status = "destroyed"
            return

        # if the bullet hits a unit, destroy the bullet and the unit
        unit = self.state.find_live_unit(new_center_pos)
        if not unit is None and unit != self.bullet.unit:
            self.bullet.status = "destroyed"
            unit.status = "destroyed"
            return

        self.bullet.position = new_pos

class DeleteDestroyedCommand(Command):
    def __init__(self, item_list):
        self.item_list = item_list

    def run(self):
        new_list = [item for item in self.item_list if item.status == "alive"]
        self.item_list[:] = new_list