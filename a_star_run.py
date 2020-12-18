import logging

import random
import pandas as pd
import matplotlib.pylab as plt
from tqdm import tqdm

import exceptions
import game
import a_star
from status import Status

from joblib import Parallel, delayed

logging.basicConfig(level=logging.ERROR)

random.seed(123)

def extract_action(head_pos, best_path):
    if len(best_path) < 2:
        return None
    diff = best_path[1] - head_pos
    if diff.x == 1:
        return 'right'
    elif diff.x == -1:
        return 'left'
    elif diff.y == 1:
        return 'down'
    else:
        return 'up'
    

def take_a_star_actions(game, render=False, save=True):
    game.game_grid.log_status(render=render, save=save)
    try:
        while True:
            try:
                best_path = a_star.a_star(
                    Status(
                        game.game_grid.snake.head_position,
                        game.game_grid.food_position,
                        game.game_grid
                    ),
                    tag_func=lambda x : hash(x.pos)
                )
                action = extract_action(
                    game.game_grid.snake.head_position, 
                    best_path.history
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

scores = []
def single_game(game_num):
    g = game.SnakeGame(game_type="a_star")
    take_a_star_actions(g)
    g.save_game(f"_{game_num}_")
    scores.append(g.game_grid.snake.length)

try:
    Parallel(n_jobs=-1)(delayed(single_game)(i) for i in tqdm(range(1_000_000_000)))
except:
    pass
finally:
    plt.hist(scores, bins=30, ec="k")
    plt.tight_layout()
    plt.gca().set(yscale="log")
    plt.show()