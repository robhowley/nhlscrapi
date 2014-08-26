
# annoying boilerplate
# get access to other sub folders
import sys
sys.path.append('..')

import nhlscrapi.constants as C
from nhlscrapi._tools import build_enum
from nhlscrapi.scrapr.rtss import RTSS


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


class Game(object):
  # add constructor argument for json source
  def __init__(self, game_key = None, extractors = {}, cum_stats = {}):
    self.plays = []
    self.game_key = game_key
    self.match_up = { 'home': '', 'away': '', 'final': { 'home': 0, 'away': 0 } }
    
    self.extractors = extractors
    self.cum_stats = cum_stats
      
  def load_plays(self):
    rtss = RTSS(self.game_key)
    
    if rtss.req_err is None:
      self.match_up = rtss.parse_matchup()
      
      for play in rtss.parsed_play_stream():
        self.__process(play, self.extractors, 'extract')
        self.__process(play, self.cum_stats, 'update')
        self.plays.append(play)
    else:
      print 'Game not found'
    
    return self.plays
  
  def __process(self, play, d, meth):
    for name, m in d.iteritems():
      getattr(m, meth)(play)
    