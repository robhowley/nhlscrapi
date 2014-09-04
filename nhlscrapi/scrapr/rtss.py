
from nhlscrapi.scrapr import playparser as pp
from nhlscrapi.scrapr.reportloader import ReportLoader

class RTSS(ReportLoader):
  """Retrieve and load RTSS play by play game data from nhl.com"""
  
  def __init__(self, game_key):
    super(RTSS, self).__init__(game_key, "rtss")

    self.plays = []
    """List of nhlscrapi.Plays loaded"""
  
  def parse_plays(self):
    """Retreive and parse Play by Play data for the given nhlscrapi.GameKey"""
    self.plays = [p for p in self.parse_plays_stream()]
    return self.plays
    
    
  def parse_plays_stream(self):
    """Generate stream of parsed plays. Useful for per play processing"""
    
    lx_doc = self.html_doc()
    
    if lx_doc is not None:
      parser = pp.PlayParser(self.game_key.season)
      plays = lx_doc.xpath('//tr[@class = "evenColor"]')
      for p in plays:
        p_obj = parser.build_play(p)
        self.plays.append(p_obj)
        
        yield p_obj