
# used by GameKey
import nhlscrapi.constants as C
from nhlscrapi._tools import build_enum

# used by Game
from nhlscrapi.games.toi import TOI
from nhlscrapi.games.rosters import Rosters
from nhlscrapi.games.playbyplay import PlayByPlay
from nhlscrapi.games.faceoffcomp import FaceOffComparison


"""Enum denoting whether the game is regular season or playoff"""
GameType = build_enum(PreSeason=1, Regular=2, Playoffs=3)


class GameKey(object):
    """Unique identifying info for a given game. (regular/playoffs, season numer, game number). TODO: JSON serializable"""
  
    def __init__(self, season = C.MIN_SEASON, game_type = GameType.Regular, game_num = 1, key_tup=None):
        """
        Initializes an unique identifier for a game. See constants for acceptable seasons and game counts. The
        key can be initialized by setting key_tup or the set of season, game type and game number.
        
        :params season: the season number denoted by year season ends
        :params game_type: enum for pre season (1), regular season (2) or playoffs (3)
        :params game_num: the index number of the game
        :params key_tup: tuple (season, game_type, game_num)
        """
        if key_tup is None:
            self.season = season
            self.game_num = game_num
            self.game_type = game_type
        else:
            self.season, self.game_num, self.game_type = key_tup
      
    @property
    def season(self):
        """
        Season of the keyed game. Season year is denoted by when the season ends. See constants for acceptable
        range of seasons considered. Not all years have supported summary reports ... or any reports at all.
        """
        return self._season
    
    @season.setter
    def season(self, value):
        if value < C.MIN_SEASON or value > C.MAX_SEASON:
            raise ValueError("Only seasons starting from " + str(C.MIN_SEASON) + " until " + str(C.MAX_SEASON))
        self._season = int(value)
  
    @property
    def game_type(self):
        """Code indicating pre season (1), regular season (2) or playoffs (3)"""
        return self._game_type
    
    @game_type.setter
    def game_type(self, value):
        if value in GameType.Name:
            self._game_type = value
        else:
            raise TypeError("GameKey.game_type must be of type GameType")
      
    def to_tuple(self):
        """Return tuple version of the game key (season, game_type, game_num"""
        return (self.season, self.game_type, self.game_num)


class Game(object):
    """
    This the primary interface to the collection of summary reports associated with every game. The
    supported reports include Play-by-play, TimeOnIce (home/away), Rosters (including coaches, officials
    and healthy scratches), and Face-off Comparison.
    
    Reports can be either lazy loaded at time of property calls or all loaded at once with load_all().
    
    Example:
    
    .. code: python
    
        from nhlscrapi.games.game import GameKey, Game
        from nhlscrapi.games.cumstats import Corsi
        
        gk = GameKey(2015, 2, 224)
        g = Game(gk, { 'Corsi': Corsi() })
        
        # since play-by-play hasn't yet been loaded the RTSS report will
        # be parsed and the Corsi computed for each team
        print(g.cum_stats['Corsi'].share())
        
        # load the rest of the reports
        g.load_all()
        
        # report back the game's linesman
        print(g.linesman)
    """
    
    def __init__(self, game_key = None, cum_stats = {}):
        """
        :params game_key: either object GameKey or (season, game_type, game_num) tuple
        :params cum_stats: dict, values are cumulative stats to be collected in play-by-play
        """
        # conversion to GameKey from tuple allowed
        self.game_key = game_key if hasattr(game_key, 'to_tuple') else GameKey(key_tup=game_key)
        
        self.toi = TOI(self.game_key)
        self.rosters = Rosters(self.game_key)
        #self.summary = GameSummary(game_key)
        self.face_off_comp = FaceOffComparison(self.game_key)
        self.play_by_play = PlayByPlay(self.game_key, None, cum_stats)
  
    
  
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
        """
        Return the game meta information displayed in report banners including team names,
        final score, game date, location, and attendance. Data format ...
        
        .. code-block:: python
        
            {
                'home': home,
                'away': away,
                'final': final,
                'attendance': att,
                'date': date,
                'location': loc
            }
        """
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
        """Return the play-by-play report object"""
        return self.play_by_play.plays()
  
  
    #@property
    #def extractors(self):
    #    return self.play_by_play.extractors
    
    
    @property
    def cum_stats(self):
        """Return the computed cumulative stats from play-by-play that were specified in the constructor"""
        return self.play_by_play.compute_stats()
  
  
    #
    # personnel related
    #
    @property
    def home_skaters(self):
        """
        Return the skaters that dressed for the home team
        
        :returns: dict keyed by player number
        """
        return self.rosters.home_skaters
    
    @property
    def home_coach(self):
        """Return the coach for the home team"""
        return self.rosters.home_coach
    
    @property
    def away_skaters(self):
        """
        Return the skaters that dressed for the away team
        
        :returns: dict keyed by player number
        """
        return self.rosters.away_skaters
  
    @property
    def away_coach(self):
        """Return the coach for the away team"""
        return self.rosters.away_coach
    
    @property
    def refs(self):
        """
        Return the refs for the game
        
        :returns: dict
        """
        return self.rosters.refs
    
    @property
    def linesman(self):
        """
        Return the linesman for the game
        
        :returns: dict
        """
        return self.rosters.linesman
  
  
    #
    # toi related
    #
    @property
    def home_toi(self):
        """
        Return the TOI shift summary for skaters on the home team
        
        :returns: dict keyed by player number
        """
        return self.toi.home_shift_summ
    
    @property
    def away_toi(self):
        """
        Return the TOI shift summary for skaters on the away team
        
        :returns: dict keyed by player number
        """
        return self.toi.away_shift_summ
    
    
    #
    # face off related
    #
    @property
    def home_fo_summ(self):
        """
        Return the home face off summary
        
        :returns: dict keyed by player number
        """
        return self.face_off_comp.home_fo
        
    @property
    def away_fo_summ(self):
        """
        Return the away face off summary
        
        :returns: dict keyed by player number
        """
        return self.face_off_comp.away_fo