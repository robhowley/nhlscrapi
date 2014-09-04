
from lxml.html import fromstring

from nhlreq import NHLCn
from nhlscrapi.scrapr import teamnameparser as TP

# enforce one method interface that fully parses doc
from abc import ABCMeta, abstractmethod

class ReportLoader(object):
  """Base class for objects that load full reports. Manages html request and extracts match up from banner"""
  
  __metaclass__ = ABCMeta
  
  __lx_doc = None
  
  def __init__(self, game_key, report_type=''):
    self.game_key = game_key
    """Game key being retrieved"""
  
    self.report_type = report_type#.lower()
    """Type of report to be loaded. Valid types correspond to the methods of NHLCn"""
  
    self.teams = { 'home': '', 'away': '' }
    """The teams in the game"""
  
    self.matchup = { 'home': '', 'away': '', 'final': { 'home': 0, 'away': 0 } }
    """Team match up and final
      {
        'home': '',
        'away': '',
        'final': { 'home': 0, 'away': 0 }
      } """
    
    self.req_err = None
    """Error from http request"""
    
    self.__have_matchup = False
      
    
  def html_doc(self):
    """Get html document"""
    
    if self.__lx_doc is None:
      cn = NHLCn()
      
      if hasattr(cn, self.report_type):
        html = getattr(cn, self.report_type)(self.game_key)
      else:
        raise ValueError('Invalid report type: %s' % self.report_type)
      
      if cn.req_err is None:
        self.__lx_doc = fromstring(html)
      else:
        self.req_err = cn.req_err
        
    return self.__lx_doc
    
    
  def parse_matchup(self):
    """Extracts and returns the matchup. Also stores it in matchup attribute."""
    lx_doc = self.html_doc()

    if lx_doc is not None:
      self.match_up = self._fill_meta(lx_doc)
      
    return self.match_up
  
  @abstractmethod
  def parse(self):
    """Fully parses html document.
    :returns: boolean success indicator
    :rtype: bool """
    self.parse_matchup()
    
    return True
    
    
  def _fill_meta(self, doc):
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

