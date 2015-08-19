
from nhlscrapi.scrapr.eventsummrep import EventSummRep
from nhlscrapi.games.repscrwrap import RepScrWrap, dispatch_loader


class EventSummary(RepScrWrap):
    """
    Event summary report. Produces the team shot/face-off summary by strength as well as the by player stats
    including scoring, TOI by situation et c.
        
    :param game_key: unique game identifier of type :py:class:`.GameKey`
    """
    
    def __init__(self, game_key):
        super(EventSummary, self).__init__(game_key, EventSummRep(game_key))
        
    @property
    @dispatch_loader('_rep_reader', 'parse_home_shots')
    def home_shots(self):
        """
        Property that returns the home team shot summary by situation.
        
        :returns: dict of the form
        
        .. code:: python
        
            {
                'home/away': {
                    'ev/pp/sh/tot': { 'won': goals, 'total': shots } },
                }
            }
        """
        return self._rep_reader.shots['home']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_away_shots')
    def away_shots(self):
        """
        Property that returns the away team shot summary by situation.
        
        """
        return self._rep_reader.shots['away']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_home_by_player')
    def home_players(self):
        return self._rep_reader.by_team['home']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_away_by_player')
    def away_players(self):
        return self._rep_reader.by_team['away']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_home_fo')
    def home_fo(self):
        return self._rep_reader.face_offs['home']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_away_fo')
    def away_fo(self):
        return self._rep_reader.face_offs['away']
    
    def __apply_to_both(self, f):
        return {
            'home': f(self.home_players),
            'away': f(self.away_players)
        }
        
    def totals(self):
        def agg(d):
            keys = ['g','a','p','pm','pn','pim','s','ab','ms','ht','gv','tk','bs']
            res = { k: 0 for k in keys }
            res['fo'] = { 'won': 0, 'total': 0 }
            for _, v in d.items():
                for k in keys:
                    res[k] += v[k]
                for fi in res['fo'].keys():
                    res['fo'][fi] += v['fo'][fi]
            return res
            
        return self.__apply_to_both(agg)
    
    def filter_players(self, pl_filter):
        def each(d):
            return {
                k: v
                for k, v in d.items()
                if pl_filter(k, v)
            }
            
        return self.__apply_to_both(each)
        
    def sort_players(self, sort_key=None, sort_func=None, reverse=False):
        def each(d):
            t = [ ]
            for num, v in d.items():
                ti = { vk: vv for vk, vv in v.items() }
                ti['num'] = num
                t.append(ti)
            
            if sort_key:
                return sorted(t, key=lambda k: k[sort_key], reverse=reverse)
            else:
                return sorted(t, key=sort_func, reverse=reverse)
            
        return self.__apply_to_both(each)
        
    def goal_scorers(self):
        return self.filter_players(
            pl_filter=lambda num, stats: stats['g']
        )
    
    def point_getters(self):
        return self.filter_players(
            pl_filter=lambda num, stats: stats['p']
        )
        
    def had_penalties(self):
        return self.filter_players(
            pl_filter=lambda num, stats: stats['pn']
        )
    
    def top_by_key(self, sort_key):
        res = self.sort_players(sort_key=sort_key, reverse=True)
        return {
            'home': res['home'][0],
            'away': res['away'][0]
        }
        
    def top_by_func(self, sort_func):
        res = self.sort_players(sort_func=sort_func, reverse=True)
        return {
            'home': res['home'][0],
            'away': res['away'][0]
        }
        
    def top_toi(self):
        return self.top_by_func(
            sort_func=lambda k: k['toi']['tot']['min']*60+k['toi']['tot']['sec']
        )
