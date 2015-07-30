
from nhlscrapi.games.toi import TOI
from nhlscrapi.games.gamekey import GameKey
from nhlscrapi.games.rosters import Rosters
from nhlscrapi.games.playbyplay import PlayByPlay
from nhlscrapi.games.faceoffcomp import FaceOffComparison


class Game(object):
  
    # add constructor argument for json source
    def __init__(self, game_key = None, extractors = {}, cum_stats = {}):
    
        # conversion to GameKey from tuple allowed
        self.game_key = game_key if hasattr(game_key, 'to_tuple') else GameKey(key_tup=game_key)
        
        self.toi = TOI(self.game_key)
        self.rosters = Rosters(self.game_key)
        #self.summary = GameSummary(game_key)
        self.face_off_comp = FaceOffComparison(self.game_key)
        self.play_by_play = PlayByPlay(self.game_key, extractors, cum_stats)
  
    
  
    def load_all(self):
        """Force all reports to be loaded and parsed instead of lazy loading on demand."""
        try:
            self.toi.load_all()
            self.rosters.load_all()
            #self.summary.load_all()
            self.play_by_play.load_all()
            self.face_off_comp.load_all()
            return self
        except Exception as e:
            print(e)
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
        elif self.toi.matchup:
            return self.toi.matchup
        else:
            self.face_off_comp.matchup
  
  
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
    
    
    #
    # face off related
    #
    @property
    def home_fo_summ(self):
        return self.face_off_comp.home_fo
        
    @property
    def away_fo_summ(self):
        return self.face_off_comp.home_fo