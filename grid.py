import os
from functools import lru_cache

import numpy as np

import exceptions
import snake

CHARACTERS = {
    "EMPTY": " ",
    "FOOD": "#",
    "SNAKE_BODY": "=",
    "SNAKE_HEAD_RIGHT": ">",
    "SNAKE_HEAD_LEFT": "<",
    "SNAKE_HEAD_UP": "^",
    "SNAKE_HEAD_DOWN": "v",
}


class GameGrid:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.all_positions = list(map(tuple, self._get_all_positions()))
        self.snake = snake.Snake(self.grid_size)
        self.game_grid = np.full((self.grid_size, self.grid_size), CHARACTERS["EMPTY"])
        self.game_grid[tuple(self.new_food_position())] = CHARACTERS["FOOD"]
        self.history = []

    def _get_all_positions(self):
        return np.array(
            np.meshgrid(range(self.grid_size), range(self.grid_size))
        ).T.reshape(-1, 2)

    def new_food_position(self, ignore_positions=None):
        if ignore_positions:
            ignore_strs = list(map(tuple, ignore_positions))
            possible_positions = [p for p in self.all_positions if p not in ignore_strs]
        else:
            possible_positions = self.all_positions
        chosen_position = possible_positions[np.random.choice(len(possible_positions))]
        return np.array(chosen_position)

    def log_status(self, render, save):
        if render:
            self.render()
        if save:
            self.history.append(self.print_grid())

    def render(self):
        print(self.print_grid())

    @staticmethod
    def insert_into_str(orig, new_char, loc):
        return orig[:loc] + new_char + orig[loc + 1 :]

    def print_grid(self):
        grid = ["".join(row) for row in self.game_grid]
        for sp in self.snake.positions:
            grid[sp[0]] = GameGrid.insert_into_str(
                grid[sp[0]], CHARACTERS["SNAKE_BODY"], sp[1]
            )
        head_char = CHARACTERS[f"SNAKE_HEAD_{self.snake.direction_string.upper()}"]
        grid[self.snake.head_position[0]] = GameGrid.insert_into_str(
            grid[self.snake.head_position[0]], head_char, self.snake.head_position[1]
        )
        hline = "*" + "-" * self.grid_size + "*"
        newline = os.linesep
        output = hline + newline
        for row in grid:
            output += "|" + row + "|" + newline
        output += hline
        return output

    def step(self):
        self.snake.move(self)

        if not self.snake.is_valid_inside_grid():
            raise exceptions.GameLostException

        if self.game_grid[tuple(self.snake.head_position)] == CHARACTERS["FOOD"]:
            self.snake.length += 1
            self.game_grid[tuple(self.snake.head_position)] = CHARACTERS["EMPTY"]
            self.game_grid[
                tuple(self.new_food_position(ignore_positions=self.snake.positions))
            ] = CHARACTERS["FOOD"]

        self.snake.clip_tail()
        if not self.snake.is_valid_crossed_itself():
            raise exceptions.GameLostException
