import logging
import random

import matplotlib.pylab as plt
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm

import a_star
import exceptions
import game
from grid import CHARACTERS

logging.basicConfig(level=logging.ERROR)

random.seed(123)


class Status(a_star.State):
    def __init__(self, pos, target, grid, history=None):
        self.pos = pos
        self.grid = grid
        self.target = target
        self.history = [] if history is None else history
        self.history.append(self.pos)

    def __lt__(self, other):
        return self.dist_to_target() > other.dist_to_target()

    def dist_to_target(self):
        return abs(self.pos - self.target)

    def is_valid(self):
        if self.pos.x < 0 or self.pos.y < 0:
            return False
        gs = self.grid.grid_size
        if self.pos.x >= gs or self.pos.y >= gs:
            return False
        if len(set(self.history)) != len(self.history):
            return False
        return self.pos not in self.grid.snake.positions[:-1]

    def all_possible_next_states(self):
        for n in self.pos.nb4():
            yield Status(n, self.target, self.grid, self.history[:])

    def is_complete(self):
        return abs(self.pos - self.target) == 1


def extract_action(head_pos, best_path):
    if len(best_path) < 2:
        return None
    diff = best_path[1] - head_pos
    if diff.x == 1:
        return "right"
    elif diff.x == -1:
        return "left"
    elif diff.y == 1:
        return "down"
    else:
        return "up"


def take_a_star_actions(game, render=False, save=True):
    game.game_grid.log_status(render=render, save=save)
    try:
        while True:
            try:
                best_path = a_star.a_star(
                    Status(
                        game.game_grid.snake.positions[-1],
                        game.game_grid.snake.positions[0],
                        game.game_grid,
                    ),
                    tag_func=lambda x: f'{x.pos}_{len(x.history)}',
                    return_status=True
                )
                action = extract_action(
                    game.game_grid.snake.head_position, best_path.history
                )
            except a_star.AStarException:
                action = None
                pass
            game.game_grid.snake.turn(action)
            game.game_grid.step()
            game.game_grid.log_status(render=render, save=save)
        return True
    except (exceptions.SnakeExitedGridException, exceptions.GameFinishedException):
        return True
    except exceptions.GameLostException:
        return False


def single_game(game_num):
    g = game.SnakeGame(game_type="longest_path")
    take_a_star_actions(g)
    g.save_game(f"_{game_num}_")


#Parallel(n_jobs=-1)(delayed(single_game)(i) for i in tqdm(range(1_000_000_000)))

single_game(0)
