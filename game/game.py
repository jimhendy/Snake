import datetime
import logging
import os
import random

import pandas as pd

from game import exceptions, grid

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class SnakeGame:

    manual_keys = {"4": "left", "6": "right", "8": "up", "2": "down"}

    def __init__(self, grid_size=10, game_type="human", random_seed=None):
        self.random_seed = random_seed
        if self.random_seed is not None:
            random.seed(self.random_seed)
        self.grid_size = grid_size
        assert 3 < self.grid_size, "Grid size must be >= 4"
        self.game_grid = grid.GameGrid(self.grid_size)
        self.game_type = game_type
        self.output_dir = os.path.join("output", self.game_type)
        self.setup_ouput()

    def setup_ouput(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def manual_run(self, render=False, save=False):
        self.game_grid.log_status(render, save)
        try:
            while True:
                self.game_grid.snake.turn(SnakeGame.wait_for_input())
                self.game_grid.step()
                self.game_grid.log_status(render, save)
        except exceptions.GameException:
            logger.info("Game Over")
            if save:
                self.save_game(f'_{self.random_seed}_')

    def save_game(self, extra_save_name=""):
        # Head Pos, Tail Pos, Food Pos, Snake Length, Grid Size
        f_name = os.path.join(
            self.output_dir,
            datetime.datetime.now().strftime(r"%Y_%m_%d_%H_%M_%S")
            + extra_save_name
            + ".csv",
        )
        with open(f_name, "w") as f:
            pd.DataFrame(self.game_grid.history).to_csv(f)

    @staticmethod
    def wait_for_input():
        while True:
            direction = input("Enter a direction to push (4, 6 ,8 ,2 ,5, q) : ")
            if direction == "q":
                raise exceptions.GameFinishedException("Game Exited")
            return SnakeGame.manual_keys.get(direction)
