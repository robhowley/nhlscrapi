
from nhlscrapi._tools import to_int
from nhlscrapi._tools import split_time
from nhlscrapi._tools import exclude_from as ex_junk

from nhlscrapi.games.plays import Strength

from nhlscrapi.scrapr.reportloader import ReportLoader
from nhlscrapi.scrapr.teamnameparser import team_abbr_parser


class GameSummRep(ReportLoader):
  """Retrieve and load game summary report from nhl.com"""
  
  def __init__(self, game_key):
    super(GameSummRep, self).__init__(game_key, 'game_summary')
    
  def parse(self):
    """Fully parses game summary report.
    :returns: boolean success indicator
    :rtype: bool """
    
    r = super(GameSummRep, self).parse()
    try:
      self.parse_scoring_summary()
      return r and False
    except:
      return False
      
      
  def parse_scoring_summary(self):
    lx_doc = self.html_doc()
    
    main = lx_doc.xpath('//*[@id="MainTable"]')[0]
    scr_summ = main.xpath('child::tr[4]//tr')
    for r in scr_summ:
      print r.get('class')
      if r.get('class') in ['oddColor','evenColor']:
        tds = r.xpath('./td')
        scr = [td.xpath('text()') for td in tds[:8]]
        
        # goal summry data
        goals = { }
        
        # goal num, game state, scoring team
        gn = to_int(scr[0][0]) if scr[0] else -1
        period = self.__period(scr[1])
        time = split_time(scr[2][0] if period < 4 else '0:00')
        strength = self.__strength(scr[3][0] if scr[3] else 'EV')
        team = team_abbr_parser(scr[4][0])
        
        # skaters on the ice
        sks = tds[8:]
        goals[gn] = {
          'per': period,
          'time': time,
          'strength': strength,
          'team': team,
          'home': self.__skaters(sks[0]),
          'away': self.__skaters(sks[1])
        }
        
        
        scorer = self.__scorer(scr[5][0])
        if scorer['num'] in goals[gn][
        assists = []
        for s in scr[6:8]:
          if s and s[0] != u'\xa0':
            print s[0], self.__scorer(s[0])
            assists.append(self.__scorer(s[0]))
          
        print {
          'goal_num': gn,
          'scorer': scorer,
          'assists': assists
        }
        
        


  def __period(self, scr):
    period = 0
    if scr:
      if scr[0] == 'SO':
        period = 5
      elif scr[0] == 'OT':
        period = 4
      else:
        period = to_int(scr[0])
      
    return period
    
  def __strength(self, sg_str):
    if 'PP' in sg_str:
      return Strength.PP
    elif 'SH' in sg_str:
      return Strength.PP
    else:
      return Strength.Even
      
  def __position(self, long_name):
    return ''.join(s[0] for s in long_name.split(' '))
    
  def __scorer(self, num_name_tot):
    nnt = num_name_tot.replace('(',' ').replace(')','')
    nnt_l = nnt.split(' ')
    return {
      'num': to_int(nnt_l[0]),
      'name': nnt_l[1].split('.')[1].strip(),
      'seas_tot': to_int(nnt_l[2]) if len(nnt_l) == 3 else -1
    }
    
  def __skaters(td):
    sk_d = { }
    for sk in td.xpath('./font'):
      pos_pl = sk.get('title').split(' - ')
      num = to_int(sk.xpath('text()')[0])
      if num > 0:
        sk_d[num] = {
          'pos': self.__position(pos_pl[0]),
          'name': pos_pl[1]
        }
        
    return sk_d