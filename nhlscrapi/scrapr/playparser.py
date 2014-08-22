
# annoying boilerplate
# get access to other sub folders
import sys
sys.path.append('../')


import nhlscrapi.constants as c
from nhlscrapi.games.plays import Play, Strength

from eventparser import event_type_mapper, parse_event_desc

class RTSSCol(object):
  def Map(season):
    if c.MIN_SEASON <= season <= c.MAX_SEASON:
      return {
          "play_num": 0,
          "per": 1,
          "str": 2,
          "time": 3,
          "event": 4,
          "desc": 5,
          "vis": 6,
          "home": 7
        }
    else:
      raise ValueError("RTSSCol.MAP(season): Invalid season " + str(season))
      
  Map = staticmethod(Map)
    

# will take a RTSS play table row and return a Play object
class PlayParser(object):
  """Interprets RTSS play by play table row and populates nhlscrapi.Play with info."""

  def __init__(self, season = c.MAX_SEASON):
    self.season = season
    
  def build_play(self, pbp_row):
    """Parses table row from RTSS
    :param pbp_row: table row from RTSS tagged with <tr class='evenColor' ... >
    :rtype: nhlscrapi.Play"""
    
    d = pbp_row.findall('./td')
    c = RTSSCol.Map(self.season)
    
    p = Play()
    p.play_num = int(d[c["play_num"]].text) if d[c["play_num"]].text.isdigit() else 0
    p.period = d[c["per"]].text
    
    p.strength = self.__strength(d[c["str"]].text)
    
    time = d[c["time"]].text.split(":")
    p.time = { "min": int(time[0]), "sec": int(time[1]) }
    
    skater_tab = d[c["vis"]].xpath("./table")
    if len(skater_tab):
      p.vis_on_ice = self.__skaters(skater_tab[0][0])
      
    skater_tab = d[c["home"]].xpath("./table")
    if len(skater_tab):
      p.home_on_ice = self.__skaters(skater_tab[0][0])
    
    p.event = event_type_mapper(d[c["event"]].text, period=p.period, skater_ct=len(p.vis_on_ice) + len(p.home_on_ice))
    p.event.desc = " ".join([str(t.encode('ascii', 'replace')) for t in d[c["desc"]].xpath("text()")])
    parse_event_desc(p.event, season=self.season)
    
    return p
  
  def __skaters(self, tab):
    """Constructs dictionary of players on the ice in the provided table at time of play.
    :param tab: RTSS table of the skaters and goalie on at the time of the play
    :rtype: dictionary, key = player number, value = [position, name]"""

    res = { }
    for td in tab.iterchildren():
      if len(td):
        pl_data = td.xpath("./table/tr")
        pl = pl_data[0].xpath("./td/font")
        
        if pl[0].text.isdigit():
          res[int(pl[0].text)] = [s.strip() for s in pl[0].get("title").split("-")][::-1]
        s = pl[0].get("title").split("-")
                
        pos = pl_data[1].getchildren()[0].text
      
    return res
    
  def __strength(self, sg_str):
    if 'PP' in sg_str:
      return Strength.PP
    elif 'SH' in sg_str:
      return Strength.PP
    else:
      return Strength.Even