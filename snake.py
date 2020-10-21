import logging

import numpy as np

import grid

logger = logging.getLogger(__name__)


class Snake:
    def __init__(self, grid_size):
        self.grid_size = grid_size

        self.direction_string = "right"
        self.directions = {
            "right": np.array([0, +1]),
            "left": np.array([0, -1]),
            "up": np.array([-1, 0]),
            "down": np.array([+1, 0]),
        }
        self.direction_step = self.directions[self.direction_string]

        self.head_position = np.array([self.grid_size // 2, self.grid_size // 2])
        self.positions = [  # Tail at the start, head at the end
            self.head_position - self.direction_step,
            self.head_position.copy(),
        ]
        self.length = len(self.positions)
        self.steps = 0
        pass

    def move(self, game_grid):
        self.head_position += self.direction_step
        self.steps += 1
        self.positions.append(self.head_position.copy())

    def clip_tail(self):
        self.positions = self.positions[-self.length :]

    def turn(self, direction_string):
        if direction_string:
            self.direction_string = direction_string
            self.direction_step = self.directions[self.direction_string]

    def is_valid_inside_grid(self):
        for pos in self.positions:
            if (
                pos[0] < 0
                or pos[1] < 0
                or pos[0] >= self.grid_size
                or pos[1] >= self.grid_size
            ):
                logger.info("Snake exited game grid")
                return False
        return True

    def is_valid_crossed_itself(self):
        if len({tuple(e) for e in self.positions}) != self.length:
            logger.info("Snake crossed itself")
            logger.info(self.positions)
            return False
        return True

