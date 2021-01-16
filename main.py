import argparse
import glob
import importlib
import os

from joblib import Parallel, delayed
from tqdm import tqdm

from game import game

parser = argparse.ArgumentParser()
parser.add_argument(
    "runner", help="Runner to use", choices=["random", "human", "bumbiter"]
)
args = parser.parse_args()

runner = importlib.import_module(f"runners.{args.runner}_run")


def single_game(game_num):
    save_name_format = f"_{game_num}_"
    if glob.glob(os.path.join("output", args.runner, f"*{save_name_format}.csv")):
        return
    g = game.SnakeGame(game_type=args.runner, random_seed=game_num)
    runner.single_game(g, save_name_format)


if args.runner != "human":
    Parallel(n_jobs=-1)(delayed(single_game)(i) for i in tqdm(range(1_000_000)))
else:
    single_game(0)
