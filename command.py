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

