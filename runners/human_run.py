from game import exceptions

def single_game(game, save_name_format):
    game.manual_run(render=True, save=True)
