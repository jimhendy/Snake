# import glob
import logging

from game import exceptions
from utils import a_star
from utils.ordered_set import OrderedSet

logging.basicConfig(level=logging.ERROR)


class Status(a_star.State):

    __slots__ = ["snake", "pos", "grid", "target", "history", "extra_history"]

    def __init__(self, snake, target, grid, history=None, extra_history=None):
        self.snake = snake  # COPY of the game.grid.snake.positions (tail at the start)
        self.pos = self.snake.last()
        self.grid = grid
        self.target = target
        self.history = OrderedSet() if history is None else history
        self.history.add(self.pos)
        self.extra_history = extra_history

    def __lt__(self, other):
        return self.dist_to_target() < other.dist_to_target()

    def dist_to_target(self):
        distance = abs(self.pos - self.target)
        if self.extra_history is None:
            return distance * self.grid.grid_size ** 2 + 1
        else:
            return distance

    def is_valid(self):
        return True

    def all_possible_next_states(self):
        for n in self.pos.nb4():

            if n.x < 0 or n.y < 0:
                continue

            if n.x >= self.grid.grid_size or n.y >= self.grid.grid_size:
                continue

            new_snake = self.snake.copy()

            if (n != self.target) or (
                (n == self.target) and (self.extra_history is not None)
            ):
                new_snake.remove_first()

            if n in new_snake:
                continue
            new_snake.add(n)

            if (n == self.target) and (self.extra_history is None):
                extra_history = self.history.copy()
                history = None
                target = self.snake.first()
            else:
                extra_history = (
                    self.extra_history
                )  # Don't need to copy as never altered
                history = self.history.copy()
                target = self.target

            yield Status(
                snake=new_snake,
                target=target,
                grid=self.grid,
                history=history,
                extra_history=extra_history,
            )

    def is_complete(self):
        return (self.pos == self.target) and (self.extra_history is not None)

    def get_steps(self):
        return self.extra_history.get() + [self.history.first()]

    def hash(self):
        hash_string = ""
        if self.extra_history is not None:
            hash_string += str(self.extra_history)
        hash_string += "@" + str(self.history)
        return hash_string


def extract_action(head_pos, next_pos):
    diff = next_pos - head_pos
    if diff.x == 1:
        return "right"
    elif diff.x == -1:
        return "left"
    elif diff.y == 1:
        return "down"
    else:
        return "up"


# @profile
def take_a_star_actions(game, render=False, save=True, max_steps=None):
    n_steps = 0
    game.game_grid.log_status(render=render, save=save)
    try:
        while True:
            try:
                best_path = a_star.a_star(
                    Status(
                        snake=game.game_grid.snake.positions,
                        target=game.game_grid.food_position,
                        grid=game.game_grid,
                    ),
                    tag_func=lambda x: x.hash(),
                    max_attempts=50_000,
                )
                actions = []
                steps = best_path.get_steps()
                for current, upcoming in zip(steps[:-1], steps[1:]):
                    actions.append(extract_action(current, upcoming))
            except a_star.AStarException:
                actions = [None]

            for a in actions:
                # print(a)
                game.game_grid.snake.turn(a)
                game.game_grid.step()
                game.game_grid.log_status(render=render, save=save)
                n_steps += 1
                if max_steps and n_steps > max_steps:
                    break

    except (exceptions.SnakeExitedGridException, exceptions.GameFinishedException):
        # print(True)
        return True
    except exceptions.GameLostException:
        # print(False)
        return False


def single_game(game, save_name_format):
    take_a_star_actions(game, max_steps=10_000)
    game.save_game(save_name_format)
