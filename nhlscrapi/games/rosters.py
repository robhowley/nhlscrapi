
from nhlscrapi.scrapr.rosterrep import RosterRep
from nhlscrapi.games.repscrwrap import RepScrWrap, dispatch_loader


class Rosters(RepScrWrap):
    """
    Roster report contains all players that dressed for the game, healthy scratches, coaches and officials. The
    roster for either home or away is returned as
    
    .. code:: python
    
        {
            player_num: {
                'pos': 'position',
                'name': 'player name'
            {
        }
        
    :param game_key: unique game identifier of type :py:class:`.GameKey`
    """
    
    def __init__(self, game_key):
        super(Rosters, self).__init__(game_key, RosterRep(game_key))
        
    @property
    @dispatch_loader('_rep_reader', 'parse_rosters')
    def home_skaters(self):
        """
        :returns: all home skaters
        :rtype: dict
        """
        return self._rep_reader.rosters['home']
        
        
    @property
    @dispatch_loader('_rep_reader', 'parse_rosters')
    def away_skaters(self):
        """
        :returns: all away skaters
        :rtype: dict
        """
        return self._rep_reader.rosters['away']
        
        
    @property
    @dispatch_loader('_rep_reader', 'parse_coaches')
    def home_coach(self):
        """
        :returns: the name of the home coach
        :rtype: string
        """
        return self._rep_reader.coaches['home']
        
        
    @property
    @dispatch_loader('_rep_reader', 'parse_coaches')
    def away_coach(self):
        """
        :returns: the name of the away coach
        :rtype: string
        """
        return self._rep_reader.coaches['away']
        
    
    @property
    @dispatch_loader('_rep_reader', 'parse_officials')
    def refs(self):
        """
        :returns: the refs for the game
        :rtype: dict, ``{ num: 'ref_name' }``
        """
        return self._rep_reader.officials['refs']
        
    
    @property
    @dispatch_loader('_rep_reader', 'parse_officials')
    def linesman(self):
        """
        :returns: the linesman for the game
        :rtype: dict, ``{ num: 'lm_name' }``
        """
        return self._rep_reader.officials['linesman']
        
        
    @property
    @dispatch_loader('_rep_reader', 'parse_scratches')
    def home_scratches(self):
        """
        :returns: all home healthy scratches
        :returns: dict
        """
        return self._roster_rep.scratches['home']
        
        
    @property
    @dispatch_loader('_rep_reader', 'parse_scratches')
    def away_scratches(self):
        """
        :returns: all away healthy scratches
        :returns: dict
        """
        return self._roster_rep.scratches['away']
