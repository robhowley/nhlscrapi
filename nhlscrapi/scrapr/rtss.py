
from lxml.html import fromstring

from nhlreq import NHLCn
from nhlscrapi.scrapr import teamnameparser as TP
from nhlscrapi.scrapr import playparser as pp


class RTSS(object):
  """Retrieve and load RTSS play by play game data from nhl.com"""
  
  __lx_doc = None
  
  def __init__(self, game_key):
    self.game_key = game_key
    """Game key being retrieved"""
    
    self.plays = []
    """List of nhlscrapi.Plays loaded"""
    
    # info to be extracted from banner
    self.match_up = {
      'home': '',
      'away': '',
      'final': { 'home': 0, 'away': 0 }
    }
  
  def html_doc(self):
    if self.__lx_doc is None:
      cn = NHLCn()
      html = cn.rtss(self.game_key)
      self.__lx_doc = fromstring(html)
      
    return self.__lx_doc
  
  def parse_matchup(self):
    lx_doc = self.html_doc()

    if lx_doc is not None:
      self.match_up = self.__fill_meta(lx_doc)
      
    return self.match_up
  
  def parse_plays(self):
    """Retreive and parse Play by Play data for the given nhlscrapi.GameKey"""
    self.plays = [p for p in self.parsed_play_stream()]
    
    
  def parsed_play_stream(self):
    """Generate stream of parsed plays. Useful for per play processing"""
    
    lx_doc = self.html_doc()
    
    if lx_doc is not None:
      
      
      parser = pp.PlayParser(self.game_key.season)
      plays = lx_doc.xpath('//tr[@class = "evenColor"]')
      for p in plays:
        p_obj = parser.build_play(p)
        self.plays.append(p_obj)
        
        yield p_obj
      
  def __fill_meta(self, doc):
    def team_scr(doc, t):
      xp = ''.join(['//table[@id="', t, '"]'])
      team = doc.xpath(xp)[0]
      team = [s for s in team.xpath('.//text()') if s.lower() != t.lower() and '\r\n' not in s and 'game' not in s.lower()]
      
      return team
      
    final = { }
    final['away'], at = tuple(team_scr(doc, 'Visitor'))
    final['home'], ht = tuple(team_scr(doc, 'Home'))
    
    away = TP.team_name_parser(at)
    home = TP.team_name_parser(ht)
    
    return {
      'home': home,
      'away': away,
      'final': final
    }