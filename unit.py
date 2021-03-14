class Unit:
    def __init__(self, state, position, tile):
        self.state = state
        self.position = position
        self.tile = tile

    def move(self, move_vector):
        raise NotImplementedError()

    def orient_weapon(self):
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

    def orient_weapon(self, target):
        self.weapon_target = target

class Tower(Unit):
    def move(self, move_vector): pass
    def orient_weapon(self, target):
        self.weapon_target = self.state.units[0].position