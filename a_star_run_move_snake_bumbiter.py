import logging
import random

from joblib import Parallel, delayed
from tqdm import tqdm

import a_star
import exceptions
import game

from collections import OrderedDict
import json

logging.basicConfig(level=logging.ERROR)

random.seed(123)


class Status(a_star.State):
    def __init__(
        self,
        snake,
        target,
        grid,
        tail_position_at_food=None,
        history=None,
        bite_bum=True
    ):
        self.snake = snake  # COPY of the game.grid.snake.positions (tail at the start)
        self.pos = self.snake[-1]
        self.grid = grid
        self.target = target
        self.history = OrderedDict() if history is None else history
        #self.history.append(self.pos)
        self.history.__setitem__(self.pos, None)
        self.tail_position_at_food = tail_position_at_food
        self.bite_bum = bite_bum

    def __lt__(self, other):
        return self.dist_to_target() < other.dist_to_target()
    
    def dist_to_target(self):
        if (not self.bite_bum) or (self.target not in self.history.keys()):
            return abs(self.pos - self.target) * self.grid.grid_size ** 2 + 1
        else:
            return abs(self.pos - self.tail_position_at_food)

    def is_valid(self):
        if self.pos.x < 0 or self.pos.y < 0:
            return False
        gs = self.grid.grid_size
        if self.pos.x >= gs or self.pos.y >= gs:
            return False
        #if len(self.history) != len(self.snake):
        #    return False
        return self.pos not in self.snake[:-1]

    def all_possible_next_states(self):
        for n in self.pos.nb4():
            new_snake = self.snake.copy()
            new_snake.append(n)
            if n != self.target:
                new_snake = new_snake[1:]
                tail_position_at_food = self.tail_position_at_food
            else:
                tail_position_at_food = self.snake[0]
            yield Status(
                new_snake,
                self.target,
                self.grid,
                tail_position_at_food,
                self.history.copy(),
                bite_bum=self.bite_bum
            )

    def is_complete(self):
        if self.bite_bum:
            return (
                self.target in self.history.keys()
                and abs(self.pos - self.tail_position_at_food) == 1
            )
        else:
            return self.pos == self.target


def extract_action(head_pos, best_path):
    if len(best_path) < 2:
        return None
    best_path.popitem(last=False)
    diff = best_path.popitem(last=False)[0] - head_pos
    if diff.x == 1:
        return "right"
    elif diff.x == -1:
        return "left"
    elif diff.y == 1:
        return "down"
    else:
        return "up"

#@profile
def take_a_star_actions(game, render=False, save=True):
    game.game_grid.log_status(render=render, save=save)
    try:
        while True:
            try:
                best_path = a_star.a_star(
                    Status(
                        game.game_grid.snake.positions,
                        game.game_grid.food_position,
                        game.game_grid,
                        bite_bum=True
                    ),
                    tag_func=lambda x: tuple(x.history.keys()),
                    max_attempts=10_000,
                )
                action = extract_action(
                    game.game_grid.snake.head_position, best_path.history
                )
            except a_star.AStarException:
                # Fallback to biting own bum
                try:
                    best_path = a_star.a_star(
                        Status(
                            game.game_grid.snake.positions,
                            game.game_grid.snake.positions[0],
                            game.game_grid,
                            bite_bum=False
                        ),
                        tag_func=lambda x: x.pos
                    )
                    action = extract_action(
                        game.game_grid.snake.head_position, best_path.history
                    )
                except a_star.AStarException:
                    # Fallback fallback to just eating the food
                    try:
                        best_path = a_star.a_star(
                            Status(
                                game.game_grid.snake.positions,
                                game.game_grid.food_position,
                                game.game_grid,
                                bite_bum=False
                            ),
                            tag_func=lambda x: x.pos
                        )
                        action = extract_action(
                            game.game_grid.snake.head_position, best_path.history
                        )
                    except a_star.AStarException:
                        # print('No solution found')
                        action = None
            # print(action)
            game.game_grid.snake.turn(action)
            game.game_grid.step()
            game.game_grid.log_status(render=render, save=save)
    except (exceptions.SnakeExitedGridException, exceptions.GameFinishedException) as e:
        # print(True)
        return True
    except exceptions.GameLostException as e:
        # print(False)
        return False


def single_game(game_num):
    g = game.SnakeGame(game_type="a_star_bumbiter", random_seed=game_num)
    take_a_star_actions(g)
    g.save_game(f"_{game_num}_")


Parallel(n_jobs=-1)(delayed(single_game)(i) for i in tqdm(range(1_000_000_000)))

#single_game(0)
