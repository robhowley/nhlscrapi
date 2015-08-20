
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
                'agg': { 'ev/pp/sh/tot': { 'g': goals, 's': shots } },
                'det': { '5v5/5v4/5v3/et c': { 'g': goals, 's': shots } }
            }
        """
        return self._rep_reader.shots['home']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_away_shots')
    def away_shots(self):
        """
        Property that returns the away team shot summary by situation.
        
        :returns: dict of the form
        
        .. code:: python
        
            {
                'agg': { 'ev/pp/sh/tot': { 'g': goals, 's': shots } },
                'det': { '5v5/5v4/5v3/et c': { 'g': goals, 's': shots } }
            }
        """
        return self._rep_reader.shots['away']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_home_by_player')
    def home_players(self):
        """
        Property that returns the home team by player summary..
        
        :returns: dict of the form
        
        .. code:: python
        
            {
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
        """
        return self._rep_reader.by_team['home']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_away_by_player')
    def away_players(self):
        """
        Property that returns the away team by player summary..
        
        :returns: dict of the form
        
        .. code:: python
        
            {
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
        """
        return self._rep_reader.by_team['away']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_home_fo')
    def home_fo(self):
        """
        Home team face off summary by strength.
        
        :returns: dict of the form
        
        .. code:: python
        
            {
                'ev/pp/sh/tot': { 'won': goals, 'total': shots }
            }
        """
        return self._rep_reader.face_offs['home']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_away_fo')
    def away_fo(self):
        """
        Away team face off summary by strength.
        
        :returns: dict of the form
        
        .. code:: python
        
            {
                'ev/pp/sh/tot': { 'won': goals, 'total': shots }
            }
        """
        return self._rep_reader.face_offs['away']
    
    def __apply_to_both(self, f):
        return {
            'home': f(self.home_players),
            'away': f(self.away_players)
        }
        
    def totals(self):
        """
        Computes and returns dictionary containing home/away by player, shots and face-off totals
        
        :returns: dict of the form ``{ 'home/away': { 'all_keys': w_numeric_data } }``
        """
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
        """
        Return the subset home and away players that satisfy the provided filter function.
        
        :param pl_filter: function that takes a by player dictionary and returns bool
        :returns: dict of the form ``{ 'home/away': { by_player_dict } }``. See :py:func:`home_players` and :py:func:`away_players`
        """
        def each(d):
            return {
                k: v
                for k, v in d.items()
                if pl_filter(k, v)
            }
            
        return self.__apply_to_both(each)
        
    def sort_players(self, sort_key=None, sort_func=None, reverse=False):
        """
        Return all home and away by player info sorted by either the provided key or function. Must provide
        at least one of the two parameters. Can sort either ascending or descending.
        
        :param sort_key: (def None) dict key to sort on
        :param sort_func: (def None) sorting function
        :param reverse: (optional, def False) if True, sort descending
        :returns: dict of the form ``{ 'home/away': { by_player_dict } }``. See :py:func:`home_players` and :py:func:`away_players`
        """
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
        """
        Return home/away by player info for the game's goal scorers.
        
        :returns: dict of the form ``{ 'home/away': { by_player_dict } }``. See :py:func:`home_players` and :py:func:`away_players`
        """
        return self.filter_players(
            pl_filter=lambda num, stats: stats['g']
        )
    
    def point_getters(self):
        """
        Return home/away by player info for the game's point getters.
        
        :returns: dict of the form ``{ 'home/away': { by_player_dict } }``. See :py:func:`home_players` and :py:func:`away_players`
        """
        return self.filter_players(
            pl_filter=lambda num, stats: stats['p']
        )
        
    def had_penalties(self):
        """
        Return home/away by player info for players who had a penalty.
        
        :returns: dict of the form ``{ 'home/away': { by_player_dict } }``. See :py:func:`home_players` and :py:func:`away_players`
        """
        return self.filter_players(
            pl_filter=lambda num, stats: stats['pn']
        )
    
    def top_by_key(self, sort_key):
        """
        Return home/away by player info for the players on each team that are first in the provided category.
        
        :param sort_key: str, the dictionary key to be sorted on
        :returns: dict of the form ``{ 'home/away': { by_player_dict } }``. See :py:func:`home_players` and :py:func:`away_players`
        """
        res = self.sort_players(sort_key=sort_key, reverse=True)
        return {
            'home': res['home'][0],
            'away': res['away'][0]
        }
        
    def top_by_func(self, sort_func):
        """
        Return home/away by player info for the players on each team who come in first according to the
        provided sorting function. Will perform ascending sort.
        
        :param sort_func: function that yields the sorting quantity
        :returns: dict of the form ``{ 'home/away': { by_player_dict } }``. See :py:func:`home_players` and :py:func:`away_players`
        """
        res = self.sort_players(sort_func=sort_func, reverse=True)
        return {
            'home': res['home'][0],
            'away': res['away'][0]
        }
        
    def top_toi(self):
        """
        Return home/away by player info for the players on each team who logged the most time on ice.
        
        :returns: dict of the form ``{ 'home/away': { by_player_dict } }``. See :py:func:`home_players` and :py:func:`away_players`
        """
        return self.top_by_func(
            sort_func=lambda k: k['toi']['tot']['min']*60+k['toi']['tot']['sec']
        )
