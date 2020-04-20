

class Error(Exception):
    pass


class GameBoardError(Error):
    pass


class GameBoardFlagLimitReached(GameBoardError):
    pass


class GameBoardDotOnMineError(GameBoardError):
    pass