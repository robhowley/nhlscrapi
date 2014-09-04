
from nhlscrapi.scrapr.reportloader import ReportLoader


class ShotSummRep(ReportLoader):
  """Retrieve and load shot summary report from nhl.com"""
  
  def __init__(self, game_key):
    super(ShotSummRep, self).__init__(game_key, 'shot_summary')
    
  def parse(self):
    r = super(ShotSummRep, self).parse()
    return r and False