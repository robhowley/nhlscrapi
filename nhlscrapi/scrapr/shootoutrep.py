
from nhlscrapi.scrapr.reportloader import ReportLoader


class ShootoutRep(ReportLoader):
  """Retrieve and load shot summary report from nhl.com"""
  
  def __init__(self, game_key):
    super(ShootoutRep, self).__init__(game_key, 'shootout')
    
  def parse(self):
    r = super(ShootoutRep, self).parse()
    return r and False