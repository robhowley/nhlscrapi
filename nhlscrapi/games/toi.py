
from nhlscrapi.scrapr.toirep import HomeTOIRep, AwayTOIRep
from nhlscrapi.games.repscrwrap import RepScrWrap, dispatch_loader


class TOI(RepScrWrap):
    def __init__(self, game_key):
        super(TOI, self).__init__(game_key, HomeTOIRep(game_key))
        
        self._away = AwayTOIRep(game_key)
        
        
    @property
    def _home(self):
        return self._rep_reader
        
        
    @property
    @dispatch_loader('_home', 'parse_shifts')
    def home_shift_summ(self):
        return self._home.by_player
        
        
    @property
    @dispatch_loader('_away', 'parse_shifts')
    def away_shift_summ(self):
        return self._away.by_player
        
        
    @property
    @dispatch_loader('_home', 'parse_shifts')
    @dispatch_loader('_away', 'parse_shifts')
    def all_toi(self):
        return {
            'home': self.home_shift_summ(),
            'away': self.away_shift_summ()
        }
        
    def load_all(self):
        if self._home.parse() and self._away.parse():
            return self
        else:
            return None
