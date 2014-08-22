
from lxml.html import fromstring

from nhlreq import NHLCn
from nhlscrapi.scrapr import playparser as pp


class RTSS(object):
  """Retrieve and load RTSS play by play game data from nhl.com"""
  
  def __init__(self, game_key):
    self.game_key = game_key
    """Game key being retrieved"""
    
    self.plays = []
    """List of nhlscrapi.Plays loaded"""
  
  def parse_plays(self):
    """Retreive and parse Play by Play data for the given nhlscrapi.GameKey"""
    self.plays = [p for p in self.parsed_play_stream()]
    
    
  def parsed_play_stream(self):
    """Generate stream of parsed plays. Useful for per play processing"""
    
    cn = NHLCn()
    html = cn.rtss(self.game_key)
    lx_doc = fromstring(html)
    
    if lx_doc is not None:
      parser = pp.PlayParser(self.game_key.season)
      plays = lx_doc.xpath('//tr[@class = "evenColor"]')
      for p in plays:
        p_obj = parser.build_play(p)
        self.plays.append(p_obj)
        
        yield p_obj
      