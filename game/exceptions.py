class GameException(Exception):
    pass


class GameFinishedException(GameException):
    pass


class GameLostException(GameException):
    pass


class SnakeAteItselfException(GameLostException):
    pass


class SnakeExitedGridException(GameLostException):
    pass
