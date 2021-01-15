from a_star import State


class Status(State):
    def __init__(self, pos, target, grid, history=None):
        self.pos = pos
        self.grid = grid
        self.target = target
        self.history = [] if history is None else history
        self.history.append(self.pos)

    def __lt__(self, other):
        return self.dist_to_target() < other.dist_to_target()

    def dist_to_target(self):
        return abs(self.pos - self.target)

    def is_valid(self):
        if self.pos.x < 0 or self.pos.y < 0:
            return False
        gs = self.grid.grid_size
        if self.pos.x >= gs or self.pos.y >= gs:
            return False
        return self.grid.snake.positions.data[self.pos] < 2

    def all_possible_next_states(self):
        for n in self.pos.nb4():
            yield Status(n, self.target, self.grid, self.history[:])

    def is_complete(self):
        return self.pos == self.target
