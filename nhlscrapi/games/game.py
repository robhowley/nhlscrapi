
# annoying boilerplate
# get access to other sub folders
import sys
sys.path.append('..')

from functools import wraps

from nhlscrapi.scrapr.rtss import RTSS
from nhlscrapi.scrapr.roster import RosterRep


class Game(object):
  
  # extracts matchup from banner if it hasn't
  # been done by another report already
  def banner_reader(rep):
    def wrapper(f):
      @wraps(f)
      def wrapped(self, *f_args, **f_kwargs):
        if not self.__have_match_up:
          attr = getattr(self, rep)
          self.match_up = attr.parse_matchup()
          self.__have_match_up = True
        return f(self, *f_args, **f_kwargs)
      return wrapped
    return wrapper
  
  # add constructor argument for json source
  def __init__(self, game_key = None, extractors = {}, cum_stats = {}):
    self.plays = []
    self.game_key = game_key
    self.match_up = { 'home': '', 'away': '', 'final': { 'home': 0, 'away': 0 } }
    
    self.extractors = extractors
    self.cum_stats = cum_stats
    
    self._rosters = RosterRep(game_key)
    
    self.__have_match_up = False
    
  #########################################
  ##
  ## RTSS Play by Play related
  ##
  #########################################
  def load_plays(self):
    rtss = RTSS(self.game_key)
    
    # only need RTSS once, so no need for banner checks
    if rtss.req_err is None:
      if not self.have_match_up:
        self.match_up = rtss.parse_matchup()
        self.have_match_up = False
      
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
  
  
  
  
  #########################################
  ##
  ## Roster Report
  ## players, scratches, coaches officials
  ##
  #########################################
  @property
  def home_roster(self):
    return self._rosters.rosters['home']
    
  @property
  def away_roster(self):
    return self._rosters.rosters['away']
  
  @banner_reader('_rosters')
  def load_rosters(self):
    return self._rosters.parse_rosters()
  
  @banner_reader('_rosters')
  def load_scratches(self):
    return self._rosters.parse_scratches()
  
  @banner_reader('_rosters')
  def load_coaches(self):
    return self._rosters.parse_coaches()
  
  @banner_reader('_rosters')
  def load_officials(self):
    return self._rosters.parse_officials()
  
  @banner_reader('_rosters')
  def load_all_personnel(self):
    return self._rosters.parse_all()
  
  
    