import logging
import random

from game import exceptions

logging.basicConfig(level=logging.ERROR)

random.seed(123)


def generate_random_actions(num=1):
    for _ in range(num):
        yield random.choice(["left", "right", "up", "down", None])


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


def single_game(game, save_name_format):
    actions = generate_random_actions(num=1_000)
    take_random_actions(game, actions)
    game.save_game(save_name_format)
