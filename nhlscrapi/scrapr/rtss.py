
from lxml.html import fromstring

from nhlscrapi.scrapr import playparser as pp


class RTSS(object):
  """Retrieve and load RTSS play by play game data from nhl.com"""
  
  def __init__(self, game_key):
    self.game_key = game_key
    """Game key being retrieved"""
    
    self.plays = []
    """List of nhlscrapi.Plays loaded"""

  @property
  def game_key(self):
    return self._game_key
    
  def parse_plays(self):
    """Retreive and parse Play by Play data for the given nhlscrapi.GameKey"""
    
    lx_doc = NHLCn().rtss(self.game_key)
    if lx_doc:
      parser = pp.PlayParser(self.game_key.season)
      plays = lx_doc.xpath('//tr[@class = "evenColor"]')
      for p in plays:
        p_obj = parser.build_play(p)
        self.plays.append(p_obj)
        
        yield p_obj
          
    return self.plays
      