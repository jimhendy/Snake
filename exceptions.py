class GameException(Exception):
    pass


class GameFinishedException(GameException):
    pass


class GameLostException(GameException):
    pass
