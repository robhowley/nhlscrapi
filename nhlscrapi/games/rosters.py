
# annoying boilerplate
# get access to other sub folders
import sys
sys.path.append('..')

from nhlscrapi.scrapr.rosterrep import RosterRep
from nhlscrapi.games.repscrwrap import RepScrWrap

class Rosters(RepScrWrap):
  
  def __init__(self, game_key):
    super(Rosters, self).__init__(game_key)
    
    self._roster_rep = RosterRep(game_key)
    
    
  @RepScrWrap.read_banner('_roster_rep')
  @RepScrWrap.lazy_load('_roster_rep', 'parse_rosters')
  def home_skaters(self):
    return self._roster_rep.rosters['home']
    
  @RepScrWrap.read_banner('_roster_rep')
  @RepScrWrap.lazy_load('_roster_rep', 'parse_rosters')
  def away_skaters(self):
    return self._roster_rep.rosters['away']
    
  @RepScrWrap.read_banner('_roster_rep')
  @RepScrWrap.lazy_load('_roster_rep', 'parse_coaches')
  def home_coach(self):
    return self._roster_rep.coaches['home']
    
  @RepScrWrap.read_banner('_roster_rep')
  @RepScrWrap.lazy_load('_roster_rep', 'parse_coaches')
  def away_coach(self):
    return self._roster_rep.coaches['away']
    
  @RepScrWrap.read_banner('_roster_rep')
  @RepScrWrap.lazy_load('_roster_rep', 'parse_officials')
  def refs(self):
    return self._roster_rep.officials['refs']
    
  @RepScrWrap.read_banner('_roster_rep')
  @RepScrWrap.lazy_load('_roster_rep', 'parse_officials')
  def linesman(self):
    return self._roster_rep.officials['linesman']
    
  @RepScrWrap.read_banner('_roster_rep')
  @RepScrWrap.lazy_load('_roster_rep', 'parse_scratches')
  def home_scratches(self):
    return self._roster_rep.scratches['home']
    
  @RepScrWrap.read_banner('_roster_rep')
  @RepScrWrap.lazy_load('_roster_rep', 'parse_scratches')
  def away_scratches(self):
    return self._roster_rep.scratches['away']