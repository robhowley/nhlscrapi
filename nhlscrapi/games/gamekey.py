

import nhlscrapi.constants as C
from nhlscrapi._tools import build_enum

"""Enum denoting whether the game is regular season or playoff"""
GameType = build_enum(Regular=2, Playoffs=3)


class GameKey(object):
    """Unique identifying info for a given game. (regular/playoffs, season numer, game number). TODO: JSON serializable"""
  
    def __init__(self, season = C.MIN_SEASON, game_type = GameType.Regular, game_num = 1, key_tup=None):
        if key_tup is None:
            self.season = season
            self.game_num = game_num
            self.game_type = game_type
        else:
            self.season, self.game_num, self.game_type = key_tup
      
    @property
    def season(self):
        return self._season
    
    @season.setter
    def season(self, value):
        if value < C.MIN_SEASON or value > C.MAX_SEASON:
            raise ValueError("Only seasons starting from " + str(C.MIN_SEASON) + " until " + str(C.MAX_SEASON))
        self._season = int(value)
  
    @property
    def game_type(self):
        return self._game_type
    
    @game_type.setter
    def game_type(self, value):
        if value in GameType.Name:
            self._game_type = value
        else:
            raise TypeError("GameKey.game_type must be of type GameType")
      
    def to_tuple(self):
        return (self.season, self.game_type, self.game_num)