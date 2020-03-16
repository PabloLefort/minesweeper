from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from .exceptions import GameBoardFlagLimitReached


class Game(models.Model):
    GAME_STARTED = 'ST'
    GAME_FINISHED = 'FI'
    GAME_STOPPED = 'SP'

    GAME_STATUSES = [
        (GAME_STARTED, 'Started'),
        (GAME_FINISHED, 'Finished'),
        (GAME_STOPPED, 'Stopped'),
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now=True)
    date_finished = models.DateTimeField(null=True)
    status = models.CharField(choices=GAME_STATUSES, default=GAME_STARTED,
                              max_length=2)
    won = models.BooleanField(default=False)

    @classmethod
    def create(cls, user):
        obj = cls(user=user)
        board = GameBoard.create(game=obj)

    def play(self, move, is_flag=False):
        board = self.gameboard_set.first()
        if is_flag:
            board.add_flag(move)
        else:
            board.add_play(move)


class GameBoard(models.Model):
    MAX_MINES = 100
    MAX_FLAGS = 100

    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    mines = models.CharField(
        validators=[validate_comma_separated_integer_list],
        default='',
        max_length=1536,
    )
    flags = models.CharField(
        validators=[validate_comma_separated_integer_list],
        default='',
        max_length=1536,
    )
    added_flags = models.PositiveIntegerField(default=MAX_FLAGS)

    @classmethod
    def create(cls, game):
        mines = cls.generate_mines()
        obj = cls(mines=mines, game=game)
        return obj

    @staticmethod
    def generate_mines():
        # Default board has 16x32 dots
        return ""
    
    def add_play(self, move):
        pass

    def add_flag(self, flag):
        if (self.added_flags - 1) == 0:
            raise GameBoardFlagLimitReached
        pass