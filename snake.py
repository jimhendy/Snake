import logging

from ordered_set import OrderedSet
from point import Point

logger = logging.getLogger(__name__)


class Snake:
    def __init__(self, grid_size):
        self.grid_size = grid_size

        self.direction_string = "right"
        self.directions = {
            "right": Point(+1, 0),
            "left": Point(-1, 0),
            "up": Point(0, -1),
            "down": Point(0, +1),
        }
        self.direction_step = self.directions[self.direction_string]

        self.head_position = Point(self.grid_size // 2, self.grid_size // 2)
        self.positions = OrderedSet(
            [  # Tail at the start, head at the end
                self.head_position - self.direction_step,
                self.head_position.copy(),
            ]
        )
        self.length = len(self.positions)
        self.steps = 0
        pass

    def move(self):
        self.head_position += self.direction_step
        self.steps += 1
        self.positions.add(self.head_position.copy())

    def clip_tail(self):
        self.positions.remove_first()

    def turn(self, direction_string):
        if direction_string:
            self.direction_string = direction_string
            self.direction_step = self.directions[self.direction_string]

    def is_valid_inside_grid(self):
        for pos in self.positions.data:
            if (
                pos.x < 0
                or pos.y < 0
                or pos.x >= self.grid_size
                or pos.y >= self.grid_size
            ):
                logger.info("Snake exited game grid")
                return False
        return True

    def is_valid_crossed_itself(self):
        if self.positions.n_unique_items() != self.positions.n_current_items:
            logger.info("Snake crossed itself")
            logger.info(self.positions)
            return False
        return True
