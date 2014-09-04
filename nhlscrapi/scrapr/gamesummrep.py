
from nhlscrapi.scrapr.reportloader import ReportLoader


class GameSummRep(ReportLoader):
  """Retrieve and load game summary report from nhl.com"""
  
  def __init__(self, game_key):
    super(GameSummRep, self).__init__(game_key, 'game_summary')
    
  def parse(self):
    r = super(GameSummRep, self).parse()
    return r and False