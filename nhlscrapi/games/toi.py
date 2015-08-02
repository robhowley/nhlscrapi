
from nhlscrapi.scrapr.toirep import HomeTOIRep, AwayTOIRep
from nhlscrapi.games.repscrwrap import RepScrWrap, dispatch_loader


class ShiftSummary(object):
    """Player's shift summary"""
  
    def __init__(self, player_num=0, player_name={ }, shifts=[], by_period={ }):
    
        self.player_num = player_num
        """The number of the player"""
        
        self.player_name = player_name
        """ Player's name: ``{ 'first': '', 'last': '' }``"""
        
        self.shifts = shifts
        """
        List of all shifts in the form
        
        .. code:: python
        
            [
                {
                    'shift_num': shift_num,
                    'period': period_num,
                    'start': start_time     # (elapsed)
                    'end': end_time         # (elapsed)
                    'dur': length_of_shift,
                    'event': EventType.Goal or EventType.Penalty
                }
            ]
        """
        
        self.by_period = by_period
        """
        Summary table by period in the form
        
        .. code:: python
        
            {
                'period': period_num,
                'shifts': shift_count,
                'avg': { 'min': min, 'sec': sec },
                'toi': { 'min': min, 'sec': sec },
                'ev_toi': { 'min': min, 'sec': sec },
                'pp_toi': { 'min': min, 'sec': sec },
                'sh_toi': { 'min': min, 'sec': sec }
            }
        """
      
    @property
    def game_summ(self):
        """
        Time on ice summary for the game
        
        :returns: dict, same form as ``self.by_period``
        """
        return self.by_period.get(0, None)


class TOI(RepScrWrap):
    """
    Time on ice summary report. Produces the time on ice per shift by player for both home and away.
        
    :param game_key: unique game identifier of type :py:class:`.GameKey`
    """
    def __init__(self, game_key):
        super(TOI, self).__init__(game_key, HomeTOIRep(game_key))
        
        self._away = AwayTOIRep(game_key)
        
        self.__wrapped_home = { }
        self.__wrapped_away = { }
    
    def __wrap(self, shift_d):
        return {
            player_num: ShiftSummary(**summ)
            for player_num, summ in shift_d.items()
        }
    
    @property
    def _home(self):
        return self._rep_reader
        
    @property
    @dispatch_loader('_home', 'parse_shifts')
    def home_shift_summ(self):
        """
        :returns: :py:class:`.ShiftSummary` by player for the home team
        :rtype: dict ``{ player_num: shift_summary_obj }``
        """
        if not self.__wrapped_home:
            self.__wrapped_home = self.__wrap(self._home.by_player)
        
        return self.__wrapped_home
        
    @property
    @dispatch_loader('_away', 'parse_shifts')
    def away_shift_summ(self):
        """
        :returns: :py:class:`.ShiftSummary` by player for the away team
        :rtype: dict ``{ player_num: shift_summary_obj }``
        """
        if not self.__wrapped_away:
            self.__wrapped_away = self.__wrap(self._away.by_player)
        
        return self.__wrapped_away
        
        
    @property
    def all_toi(self):
        """
        Return
    
        :returns: the :py:class:`scrapr.toi.ShiftSummary` by player for the home/away team
        :rtype: dict ``{ 'home/away': { player_num: shift_summary_obj } }``
        """
        return {
            'home': self.home_shift_summ(),
            'away': self.away_shift_summ()
        }
        
    def load_all(self):
        """
        Loads all parts of the report.
        
        :returns: ``self`` or ``None`` if load fails
        """
        if self._home.parse() and self._away.parse():
            return self
        else:
            return None
