import logging

import numpy as np
import pandas as pd
from tqdm import tqdm

import exceptions
import game

logging.basicConfig(level=logging.ERROR)


def generate_random_actions(p=0.05, num=1):
    return np.random.choice(
        ["left", "right", "up", "down", None], p=[p] * 4 + [1 - 4 * p], size=num
    )


def take_random_actions(game, actions, render=False, save=True):
    game.game_grid.log_status(render=render, save=save)
    try:
        for action in actions:
            game.game_grid.snake.turn(action)
            game.game_grid.step()
            game.game_grid.log_status(render=render, save=save)
        return True
    except exceptions.GameException:
        return False


scores = []
for game_num in tqdm(range(1_000)):
    g = game.SnakeGame(game_type="random")
    actions = generate_random_actions(num=100)
    take_random_actions(g, actions)
    s = g.game_grid.snake.length
    if s > 2:
        g.save_game(f'_{game_num}_')
    scores.append(s)

print(pd.Series(scores).value_counts())
