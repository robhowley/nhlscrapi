
from itertools import chain

from nhlscrapi._tools import (
    to_int,
#    re_comp_num_pos_name,
    exclude_from as ex_junk
)
from nhlscrapi.scrapr.reportloader import ReportLoader


def _rem(txt):
    return ex_junk(txt, containing=['\n','\r'])
    
    
def _zip_top_bot(txt_lst):
    cols = len(txt_lst)/2
    return [ (k,v) for k, v in zip(txt_lst[:cols],txt_lst[cols:]) ]
    

class EventSummRep(ReportLoader):
    """Retrieve and load event summary report from nhl.com"""
    
    def __init__(self, game_key):
        super(EventSummRep, self).__init__(game_key, 'event_summary')
        
        self.shots = { }
        """
        The shot summary by strength at the aggregate and detail level
        
        :returns: dict of the form
        
        .. code:: python
        
            {
                'home/away': {
                    'agg': { 'ev/pp/sh/tot': { 'g': goals, 's': shots } },
                    'det': { '5v5/5v4/5v3/et c': { 'g': goals, 's': shots } }
                }
            }
        """
        
        self.face_offs = { }
        """
        Face off summary by strength.
        
        :returns: dict of the form
        
        .. code:: python
        
            {
                'home/away': {
                    'ev/pp/sh/tot': { 'won': goals, 'total': shots } },
                }
            }
        """
        
        self.by_team = { }
        """
        By player team summary.
        
        :returns: dict of the form
        
        .. code:: python
        
            {
                'home/away': {
                    'num': {
                        'pos': pos,
                        'name': { 'first': first, 'last': last },
                        'g/a/p/pm/pn/pim/shifts/s/ab/ms/ht/gv/tk/bs': value
                        'fo': { 'won': won, 'tot': total },
                        'toi': {
                            'tot/avg/pp/sh/ev': { 'min': mins, 'sec': secs }
                        }
                    }
                }
            }
        """
        
        # define place holders for different parts of the report
        # each one corresponds to a bit of data that can be parsed individually
        self.__aw_top, self.__aw_bot, self.__h_top, self.__h_bot = [None]*4  # shot summ
        self.__away_fo, self.__home_fo = [None]*2  # face off summ
        
    def parse(self):
        """
        Retreive and parse Event Summary report for the given :py:class:`nhlscrapi.games.game.GameKey`
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        try:
            return super(EventSummRep, self).parse() \
                .parse_away_shots() \
                .parse_home_shots() \
                .parse_away_fo() \
                .parse_home_fo() \
                .parse_away_by_player() \
                .parse_home_by_player()
        except:
            return None
    
    def __get_tr_by_name(self, name):
        xp = ".//td[contains(./text(),'{}')]/../following-sibling::tr".format(name)
        return self.html_doc().xpath(xp)[0]
        
    def __set_shot_tables(self):
        if self.__aw_top is None:
            shot_tr = self.__get_tr_by_name('SHOTS SUMM')
            _ , self.__aw_top, self.__aw_bot, self.__home_top, self.__home_bot = shot_tr.xpath('.//table')
            
    def __parse_shot_tables(self, top_table, bot_table):
        def key_g_s(rows_lst):
            res = { }
            for k, v in _zip_top_bot(_rem(rows_lst)):
                g, s = v.split('-') if '-' in v else ('0', '0')
                res[k.lower()] = { 'g': to_int(g, 0), 's': to_int(s, 0) }
            return res
        
        return {
            'agg': key_g_s(top_table.xpath('.//text()')),
            'det': key_g_s(bot_table.xpath('.//text()'))
        }
        
    def __set_fo_tables(self):
        if self.__away_fo is None:
            fo_tr = self.__get_tr_by_name('FACE-OFF')
            _, self.__away_fo, self.__home_fo = fo_tr.xpath('.//table')
        
    def __parse_fo_table(self, table):
        def str_w_t(rows_lst):
            res = { }
            for k, v in _zip_top_bot(_rem(rows_lst)):
                ct, _ = v.split('/') if '/' in  v else ('0-0','0')
                w, t = ct.split('-') if '-' in v else ('0', '0')
                res[k.lower()] = { 'won': to_int(w, 0), 'total': to_int(t, 0) }
            return res
            
        return str_w_t(table.xpath('.//text()'))
        
    def __set_team_tables(self):
        if self.__away is None:
            team_tr = self.__get_tr_by_name('TEAM')
            _, self.__away, self.__home = team_tr.xpath('.//table')
        
    def __parse_team_tables(self, table):
        pass
    
    def parse_home_shots(self):
        """
        Parse shot info for home team.
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        try:
            self.__set_shot_tables()
            self.shots['home'] = self.__parse_shot_tables(
                self.__home_top,
                self.__home_bot
            )
            return self
        except:
            return None
    
    def parse_away_shots(self):
        """
        Parse shot info for away team.
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        try:
            self.__set_shot_tables()
            self.shots['away'] = self.__parse_shot_tables(
                self.__aw_top,
                self.__aw_bot
            )
            return self
        except:
            return None
        
    def parse_home_fo(self):
        """
        Parse face-off info for home team.
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        try:
            self.__set_fo_tables()
            self.face_offs['home'] = self.__parse_fo_table(self.__home_fo)
            return self
        except:
            return None
            
    def parse_away_fo(self):
        """
        Parse face-off info for away team.
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        try:
            self.__set_fo_tables()
            self.face_offs['away'] = self.__parse_fo_table(self.__away_fo)
            return self
        except:
            return None
        
    def __read_line(self, tr):
        rec = _rem(tr.xpath('.//text()'))
        if len(rec) == 25:
            # player info
            num = to_int(rec[0],0)
            if not num:
                return { }
                
            dat = { }
            dat['pos'] = rec[1]
            
            last, first = rec[2].split(',')
            dat['name'] = { 'first': first.strip(), 'last': last.strip() }
            
            dat['shifts'] = to_int(rec[10],0)
            
            cols = chain(
                [ (i+3,v) for i,v in enumerate(['g','a','p','pm','pn','pim']) ],
                [ (i+15,v) for i,v in enumerate(['s','ab','ms','ht','gv','tk','bs']) ]
            )
            for i, col in cols:
                dat[col] = to_int(rec[i],0)
            
            dat['toi'] = { }
            for k, v in [ (9,'tot'), (11,'avg'), (12,'pp'), (13,'sh'), (14,'ev') ]:
                if ':' in rec[k]:
                    mins, secs = rec[k].split(':')
                    dat['toi'][v] = { 'min': to_int(mins,0), 'sec': to_int(secs,0) }
                else:
                    dat['toi'][v] = { 'min': 0, 'sec': 0 }
            
            w, l = to_int(rec[22],0), to_int(rec[23],0)
            dat['fo'] = { 'won': w, 'total': w+l }
            
            return num, dat
        else:
            return -1, { }

    def __parse_players(self):
        bp_tr = self.__get_tr_by_name('TEAM SUMM')
        all_bp = bp_tr.xpath(".//tr[contains(@class,'Color')]")
        
        t = 'away'
        self.by_team = { 'home': { }, 'away': { } }
        for abp in all_bp:
            num, p = self.__read_line(abp)
            if num == -1:
                t = 'home'
            else:
                self.by_team[t][num] = p
            
    def parse_home_by_player(self):
        """
        Parse by player info for home team.
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        try:
            if not self.by_team:
                self.__parse_players()
            
            return self
        except:
            return None
            
    def parse_away_by_player(self):
        """
        Parse by player info for away team.
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        try:
            if not self.by_team is None:
                self.__parse_players()
            
            return self
        except:
            return None
