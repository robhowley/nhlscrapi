
from nhlscrapi.games.toi import TOI
from nhlscrapi.games.gamekey import GameKey
from nhlscrapi.games.rosters import Rosters
from nhlscrapi.games.playbyplay import PlayByPlay


class Game(object):
  
    # add constructor argument for json source
    def __init__(self, game_key = None, extractors = {}, cum_stats = {}):
    
        if hasattr(game_key, 'to_tuple'):
            self.game_key = game_key
        else:
            self.game_key = GameKey(key_tup=game_key)
        
        self.toi = TOI(game_key)
        self.rosters = Rosters(game_key)
        #self.summary = GameSummary(game_key)
        self.play_by_play = PlayByPlay(game_key, extractors, cum_stats)
  
    
  
    def load_all(self):
        """Force all reports to be loaded and parsed instead of lazy loading on demand."""
        try:
            self.toi.load_all()
            self.rosters.load_all()
            self.summary.load_all()
            self.play_by_play.load_all()
            return self
        except:
            return None
  
  
    #########################################
    ##
    ## convenience wrapper properties
    ##
    #########################################
    @property
    def matchup(self):
        if self.play_by_play.matchup:
            return self.play_by_play.matchup
        elif self.rosters.matchup:
            return self.rosters.matchup
        else:
            return self.toi.matchup
  
  
    #
    # play related
    #
    @property
    def plays(self):
        return self.play_by_play.plays()
  
  
    @property
    def extractors(self):
        return self.play_by_play.extractors
    
    
    @property
    def cum_stats(self):
        return self.play_by_play.compute_stats()
  
  
    #
    # personnel related
    #
    @property
    def home_skaters(self):
        return self.rosters.home_skaters
    
    @property
    def home_coach(self):
        return self.rosters.home_coach
    
    @property
    def away_skaters(self):
        return self.rosters.away_skaters
  
    @property
    def away_coach(self):
        return self.rosters.away_coach
    
    @property
    def refs(self):
        return self.rosters.refs
    
    @property
    def linesman(self):
        return self.rosters.linesman
  
  
    #
    # toi related
    #
    @property
    def home_toi(self):
        return self.toi.home_shift_summ
    
    @property
    def away_toi(self):
        return self.toi.away_shift_summ
    