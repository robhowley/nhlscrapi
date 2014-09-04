
# annoying boilerplate
# get access to other sub folders
import sys
sys.path.append('..')

from nhlscrapi.scrapr.toirep import HomeTOIRep, AwayTOIRep
from nhlscrapi.games.repscrwrap import RepScrWrap

class TOI(RepScrWrap):
  
  def __init__(self, game_key):
    super(TOI, self).__init__(game_key)
    
    self._home = HomeTOIRep(game_key)
    self._away = AwayTOIRep(game_key)
  
  @RepScrWrap.read_banner('_home')
  @RepScrWrap.lazy_load('_home', 'parse_shifts')
  def home_shift_summ(self):
    return self._home.by_player
    
  @RepScrWrap.read_banner('_away')
  @RepScrWrap.lazy_load('_away', 'parse_shifts')
  def away_shift_summ(self):
    return self._away.by_player

  @RepScrWrap.read_banner('_home')
  @RepScrWrap.read_banner('_away')
  @RepScrWrap.lazy_load('_home', 'parse_shifts')
  @RepScrWrap.lazy_load('_away', 'parse_shifts')
  def all_toi(self):
    return {
      'home': self.load_home(),
      'away': self.load_away()
    }