
from nhlscrapi.scrapr.reportloader import ReportLoader


class EventSummRep(ReportLoader):
  """Retrieve and load event summary report from nhl.com"""
  
  def __init__(self, game_key):
    super(EventSummRep, self).__init__(game_key, 'event_summary')
    
  def parse(self):
    r = super(EventSummRep, self).parse()
    return r and False