import logging

import random
import pandas as pd
import matplotlib.pylab as plt
from tqdm import tqdm

import exceptions
import game

from joblib import Parallel, delayed

logging.basicConfig(level=logging.ERROR)

random.seed(123)


def generate_random_actions(num=1):
    for _ in range(num):
        yield random.choice(
            ["left", "right", "up", "down", None]
        )

#@profile
def take_random_actions(game, actions, render=False, save=True):
    game.game_grid.log_status(render=render, save=save)
    try:
        for action in actions:
            game.game_grid.snake.turn(action)
            game.game_grid.step()
            game.game_grid.log_status(render=render, save=save)
        return True
    except (exceptions.SnakeExitedGridException, exceptions.GameFinishedException):
        return True
    except exceptions.GameLostException:
        return False

def single_game(game_num):
    g = game.SnakeGame(game_type="random")
    actions = generate_random_actions(num=10)
    save_game = take_random_actions(g, actions)
    score = g.game_grid.snake.length
    steps = g.game_grid.snake.steps
    if save_game and score >= 4 and steps > (g.grid_size - g.grid_size // 2):
        g.save_game(f"_{game_num}_")
        pass
    return score


scores = Parallel(n_jobs=-1)( delayed(single_game)(i) for i in tqdm(range(1_000_000_000)))

plt.hist(scores, bins=30, ec="k")
plt.tight_layout()
plt.gca().set(yscale="log")
plt.show()
