import os
# import numpy as np
import random
from functools import lru_cache

import exceptions
import snake
from point import Point

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
        self.snake = snake.Snake(self.grid_size)
        self.game_grid = [
            [CHARACTERS["EMPTY"] for col in range(self.grid_size)]
            for row in range(self.grid_size)
        ]
        self.food_position = None  # Set inside new_food_position
        self.set_char(
            self.new_food_position(ignore_positions=self.snake.positions),
            CHARACTERS["FOOD"],
        )
        self.history = []

    def set_char(self, pt, char):
        self.game_grid[pt.y][pt.x] = char

    def get_char(self, pt):
        return self.game_grid[pt.y][pt.x]

    def new_food_position(self, ignore_positions=None):
        while True:
            chosen_position = Point(
                random.randint(0, self.grid_size - 1),
                random.randint(0, self.grid_size - 1),
            )
            if ignore_positions is None or chosen_position not in ignore_positions:
                break
        self.food_position = chosen_position
        return chosen_position

    def log_status(self, render, save):
        if render:
            self.render()
        if save:
            self.history.append(
                {
                    "Head_Pos_x": self.snake.head_position.x,
                    "Head_Pos_y": self.snake.head_position.y,
                    "Tail_Pos_x": self.snake.positions[0].x,
                    "Tail_Pos_y": self.snake.positions[0].y,
                    "Food_Pos_x": self.food_position.x,
                    "Food_Pos_y": self.food_position.y,
                    "Snake_Length": len(self.snake.positions),
                    "Grid_Size": self.grid_size,
                }
            )

    def render(self):
        print(self.print_grid())

    @staticmethod
    def insert_into_str(orig, new_char, loc):
        return orig[:loc] + new_char + orig[loc + 1 :]

    def print_grid(self):
        grid = ["".join(row) for row in self.game_grid]
        for sp in self.snake.positions:
            grid[sp.y] = GameGrid.insert_into_str(
                grid[sp.y], CHARACTERS["SNAKE_BODY"], sp.x
            )
        head_char = CHARACTERS[f"SNAKE_HEAD_{self.snake.direction_string.upper()}"]
        hp = self.snake.head_position
        grid[hp.y] = GameGrid.insert_into_str(grid[hp.y], head_char, hp.x)
        hline = "*" + "-" * self.grid_size + "*"
        newline = os.linesep
        output = hline + newline
        for row in grid:
            output += "|" + row + "|" + newline
        output += hline
        return output

    # @profile
    def step(self):
        self.snake.move(self)

        if not self.snake.is_valid_inside_grid():
            raise exceptions.GameLostException

        if self.get_char(self.snake.head_position) == CHARACTERS["FOOD"]:
            self.snake.length += 1
            self.set_char(self.snake.head_position, CHARACTERS["EMPTY"])
            self.set_char(
                self.new_food_position(ignore_positions=self.snake.positions),
                CHARACTERS["FOOD"],
            )
        self.snake.clip_tail()

        if not self.snake.is_valid_crossed_itself():
            raise exceptions.GameLostException
