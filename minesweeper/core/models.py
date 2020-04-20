import random

from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from functools import reduce
from picklefield.fields import PickledObjectField

from .exceptions import (
    GameBoardFlagLimitReached,
    GameBoardDotOnMineError,
)


class Game(models.Model):
    GAME_STARTED = 'ST'
    GAME_FINISHED = 'FI'
    GAME_STOPPED = 'SP'

    GAME_STATUSES = [
        (GAME_STARTED, 'Started'),
        (GAME_FINISHED, 'Finished'),
        (GAME_STOPPED, 'Stopped'),
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    date_created = models.DateTimeField(auto_now=True)
    date_finished = models.DateTimeField(null=True)
    status = models.CharField(choices=GAME_STATUSES, default=GAME_STARTED,
                              max_length=2)
    won = models.BooleanField(default=False)

    @classmethod
    def create(cls, user=None):
        obj = cls(user=user)
        obj.save()
        board = GameBoard.create(game=obj)
        return obj

    def play(self, x, y, is_flag=False):
        board = self.gameboard_set.first()
        if is_flag:
            board.add_flag(x, y)
        else:
            board.add_play(x, y)


class GameBoard(models.Model):
    DEFAULT_MAX_MINES = 100
    DEFAULT_MAX_FLAGS = 100
    DEFAULT_ROWS = 16
    DEFAULT_COLUMNS = 32

    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    mines = models.CharField(
        default='',
        max_length=4096,
    )
    plays = PickledObjectField(null=True)
    rows = models.PositiveIntegerField(default=DEFAULT_ROWS)
    columns = models.PositiveIntegerField(default=DEFAULT_COLUMNS)
    added_flags = models.PositiveIntegerField(default=DEFAULT_MAX_FLAGS)

    @classmethod
    def create(cls, game, max_flags=DEFAULT_MAX_FLAGS, max_mines=DEFAULT_MAX_MINES,
               columns=DEFAULT_COLUMNS, rows=DEFAULT_ROWS):
        mines = cls.generate_mines(1, rows, columns)
        # Add check of (rows x columns) - mines > 1 when passing those kwargs
        obj = cls(mines=mines, game=game)
        obj.save()
        return obj

    @staticmethod
    def generate_mines(max_mines, rows, columns):
        mines_dict = {}
        mines = ''
        mines_count = 0
        while mines_count < max_mines:
            x = int(random.randint(0, columns))
            y = int(random.randint(0, rows))
            new = f'{x};{y}'
            if not hasattr(mines, new):
                mines_dict[new] = 0
                mines_count += 1
                mines = f'{mines}{new},' if (mines_count + 1) < max_mines else f'{mines}{new}'

        return mines

    def parse_mines(self):
        mines = set()
        for i in self.mines.split(','):
            mines.add(i)
        return mines

    def add_play(self, x, y):
        mines = self.parse_mines()
        for_process, dot_mines = self._process_dot(x, y, mines)
        if dot_mines:
            raise GameBoardDotOnMineError
        else:
            processing = True
            new_plays = {}
            visited = set()
            while processing:
                new_ones = set()
                for dot in for_process:
                    visited.add(dot)
                    x, y = (int(i) for i in dot.split(';'))
                    new_ones_from_dot, dot_mines = self._process_dot(x, y, mines)
                    if dot_mines:
                        new_plays[dot] = dot_mines
                        continue
                    else:
                        new_ones = new_ones.union(new_ones_from_dot)

                if len(new_ones):
                    for_process = new_ones.difference(for_process)
                    for_process = for_process.difference(visited)
                else:
                    processing = False

            # TODO: save new plays

    def _process_dot(self, x, y, mines):
        adjacents = self._get_adjacents(x, y)
        dot_mines = len(adjacents.intersection(mines))
        return adjacents, dot_mines

    def _get_adjacents(self, x, y):
        adjacents = set()
        for i in range(9):
            if i <= 2:
                aux_y = y + 1
                aux_x = x - 1 + i
            elif i <= 5:
                aux_y = y
                aux_x = x - 4 + i
            elif i <= 8:
                aux_y = y - 1
                aux_x = x - 7 + i
            if aux_y == y and aux_x == x:
                continue
            elif aux_y < self.rows and aux_y >= 0 and aux_x < self.columns and aux_x >= 0:
                adjacents.add(f'{aux_x};{aux_y}')
        return adjacents 

    def add_flag(self, x, y):
        # TODO: add the flag to self.plays
        if (self.added_flags - 1) == 0:
            raise GameBoardFlagLimitReached
        else:
            self.added_flags -= 1
            # check if deleting the flag and then move to mines check
            mines = self.parse_mines()
            try:
                mines.pop(f'{x};{y}')
                self.mines = reduce(lambda k, j: k + ',' + j, mines)
            except KeyError:
                pass

            self.save()
