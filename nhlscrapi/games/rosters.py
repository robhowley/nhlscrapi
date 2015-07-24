
from nhlscrapi.scrapr.rosterrep import RosterRep
from nhlscrapi.games.repscrwrap import RepScrWrap, dispatch_loader


class Rosters(RepScrWrap):
    def __init__(self, game_key):
        super(Rosters, self).__init__(game_key, RosterRep(game_key))
        
    
    @property
    @dispatch_loader('_rep_reader', 'parse_rosters')
    def home_skaters(self):
        return self._rep_reader.rosters['home']
        
        
    @property
    @dispatch_loader('_rep_reader', 'parse_rosters')
    def home_skaters(self):
        return self._rep_reader.rosters['away']
        
        
    @property
    @dispatch_loader('_rep_reader', 'parse_coaches')
    def home_coach(self):
        return self._rep_reader.coaches['home']
        
        
    @property
    @dispatch_loader('_rep_reader', 'parse_coaches')
    def away_coach(self):
        return self._rep_reader.coaches['away']
        
    
    @property
    @dispatch_loader('_rep_reader', 'parse_officials')
    def refs(self):
        return self._rep_reader.officials['refs']
        
    
    @property
    @dispatch_loader('_rep_reader', 'parse_officials')
    def linesman(self):
        return self._rep_reader.officials['linesman']
        
        
    @property
    @dispatch_loader('_rep_reader', 'parse_scratches')
    def home_scratches(self):
        return self._roster_rep.scratches['home']
        
        
    @property
    @dispatch_loader('_rep_reader', 'parse_scratches')
    def away_scratches(self):
        return self._roster_rep.scratches['away']
