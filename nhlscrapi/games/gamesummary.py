
# annoying boilerplate
# get access to other sub folders
import sys
sys.path.append('..')

from nhlscrapi.scrapr.summrep import SummaryRep
from nhlscrapi.games.repscrwrap import RepScrWrap

class GameSummary(RepScrWrap):
  
  def __init__(self, game_key):
    super(GameSummary, self).__init__(game_key)
    
    self._summary_rep = SummaryRep(game_key)
    
#  @RepScrWrap.read_banner('_roster_rep')
#  @RepScrWrap.lazy_load('_roster_rep', 'parse_rosters')