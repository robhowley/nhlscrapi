
import re

from lxml.html import fromstring

from nhlscrapi.scrapr.nhlreq import NHLCn
from nhlscrapi.scrapr import teamnameparser as TP

# enforce one method interface that fully parses doc
from abc import ABCMeta, abstractmethod


class ReportLoader(object):
    """
    Base class for objects that load full reports. Manages html request and extracts match up from banner
    
    :param game_key: unique game identifier of type :py:class:`nhlscrapi.games.game.GameKey`
    :param report_type: str, type of report being loaded. Must be a method of :py:class:`.NHLCn`
    """
  
    __metaclass__ = ABCMeta
    __lx_doc = None
 
    def __init__(self, game_key, report_type=''):
        self.game_key = game_key
        """Game key being retrieved of type :py:class:`nhlscrapi.games.game.GameKey` """
      
        self.report_type = report_type
        """Type of report to be loaded. Valid types correspond to the methods of :py:class:`.NHLCn`"""
        
        self.matchup = { }
        """
        Fame meta information displayed in report banners including team names,
        final score, game date, location, and attendance. Data format is
        
        .. code:: python
        
            {
                'home': home,
                'away': away,
                'final': final,
                'attendance': att,
                'date': date,
                'location': loc
            }
        """
        
        self.req_err = None
        """Error from http request"""
      
    
    def html_doc(self):
        """
        :returns: the lxml processed html document
        :rtype: ``lxml.html.document_fromstring`` output
        """
        
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
        """
        Parse the banner matchup meta info for the game.
        
        :returns: ``self`` on success or ``None``
        """
        lx_doc = self.html_doc()
        try:
            if not self.matchup:
                self.matchup = self._fill_meta(lx_doc)
            return self
        except:
            return None
        
        
    @abstractmethod
    def parse(self):
        """
        Fully parses html document.
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        
        return self.parse_matchup()
    
    
    def _fill_meta(self, doc):
        def team_scr(doc, t):
            xp = ''.join(['//table[@id="', t, '"]'])
            team = doc.xpath(xp)[0]
            team = [s for s in team.xpath('.//text()') if s.lower() != t.lower() and '\r\n' not in s and 'game' not in s.lower()]
      
            return team
      
        final = { }
        final['away'], at = tuple(team_scr(doc, 'Visitor'))
        final['home'], ht = tuple(team_scr(doc, 'Home'))
    
        # clean team names
        away = TP.team_name_parser(at)
        home = TP.team_name_parser(ht)
        
        game_info = doc.xpath('//table[@id="GameInfo"]')[0].xpath('.//text()')
        game_info = '; '.join(s.strip() for s in game_info if s.strip() != '')
        
        att = re.findall(r'(?<=[aA]ttendance\s)(\d*\,?\d*)', game_info)
        att = int(att[0].replace(',','')) if att else 0
        
        date = re.findall(r'\w+\,?\s\w+\s\d+\,?\s\d+', game_info)
        date = date[0] if date else ''
        
        loc = re.findall(r'(?<=at\W)([^\;]*)', game_info)
        loc = loc[0] if loc else ''
    
        return {
            'home': home,
            'away': away,
            'final': final,
            'attendance': att,
            'date': date,
            'location': loc
        }

