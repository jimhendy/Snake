import datetime
import logging
import os

import exceptions
import grid

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class SnakeGame:
    #@profile
    def __init__(self, grid_size=10, game_type="human"):
        self.grid_size = grid_size
        assert 3 < self.grid_size, "Grid size must be >= 4"
        self.game_grid = grid.GameGrid(self.grid_size)
        self.game_type = game_type
        self.output_dir = os.path.join("output", self.game_type)
        self.setup_ouput()

    def setup_ouput(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def run(self, render=False, save=False):
        self.game_grid.log_status(render, save)
        try:
            while True:
                self.game_grid.snake.turn(SnakeGame.wait_for_input())
                self.game_grid.step()
                self.game_grid.log_status(render, save)
        except exceptions.GameException:
            logger.info("Game Over")

    def save_game(self, extra_save_name=''):
        f_name = os.path.join(
            self.output_dir, datetime.datetime.now().strftime(r"%Y_%m_%d_%H_%M_%S") + extra_save_name + '.txt'
        )
        with open(f_name, "w") as f:
            f.write(os.linesep.join(self.game_grid.history))

    @staticmethod
    def wait_for_input():
        while True:
            try:
                direction = input("Enter a direction to push (4, 6 ,8 ,2 ,5, q) : ")
                if direction == "q":
                    raise exceptions.GameFinishedException("Game Exited")
                return {"4": "left", "6": "right", "8": "up", "2": "down"}.get(
                    direction
                )
            except KeyError:
                print('Error, enter "l","r" or nothing')

