
from nhlscrapi.scrapr.reportloader import ReportLoader


class FaceOffRep(ReportLoader):
  """Retrieve and load face-off comparison report from nhl.com"""
  
  def __init__(self, game_key):
    super(FaceOffRep, self).__init__(game_key, 'face_offs')
    
  def parse(self):
    r = super(FaceOffRep, self).parse()
    return r and False