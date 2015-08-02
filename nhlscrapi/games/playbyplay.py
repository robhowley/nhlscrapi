
from nhlscrapi._tools import build_enum

from nhlscrapi.scrapr.rtss import RTSS
from nhlscrapi.games.repscrwrap import RepScrWrap
  
Strength = build_enum('Even', 'PP', 'SH')
"""Enum indicating play strength."""

class Play(object):
    """Contains base level of state info about a given play"""
    def __init__(self,
            play_num=0, period=0, strength=Strength.Even, time={ "min": 20, "sec": 0 },
            vis_on_ice = { }, home_on_ice = { }, event=None):
                
        self.play_num = play_num
        """Number of player who made the play"""
        
        self.period = period
        """Current period"""
        
        self.strength = strength
        """Enum indicating either even strength, shorthanded, or power play"""
        
        self.time = time
        """Time remaining in the period"""
        
        self.vis_on_ice = vis_on_ice
        """All players on the visiting team on the ice at the time. ``{ num: [position, name] }``"""
        
        self.home_on_ice = home_on_ice
        """All players on the home team on the ice at the time. ``{ num: [position, name] }``"""
        
        self.event = event
        """
        An object that inherits from :py:class:`.Event` that contains other specifics related to
        the given type of play
        """

class PlayByPlay(RepScrWrap):
    def __init__(self, game_key, extractors = {}, cum_stats = {}, init_cs_teams=True):
        super(PlayByPlay, self).__init__(game_key, RTSS(game_key))
        
        #    self._rtss = RTSS(game_key)
        self.extractors = extractors
        self.cum_stats = cum_stats
        self.init_cs_teams = init_cs_teams
        self.__have_stats = False
        
        self.__wrapped_plays = []
    
    # doesn't need to be dispatched
    # this is managed by compute_stats
    @property
    def plays(self):
        self.compute_stats()
        return self.__wrapped_plays
        
        
    def compute_stats(self):
        if not self.__have_stats:
            if self.init_cs_teams and self.cum_stats:
                self.__init_cs_teams()
            
            for play in self._rep_reader.parse_plays_stream():
                p = Play(**play)
                self.__wrapped_plays.append(p)
                if self.extractors:
                    self.__process(p, self.extractors, 'extract')
                if self.cum_stats:
                    self.__process(p, self.cum_stats, 'update')
                self.__have_stats = True
                
        return self.cum_stats
        
        
    def __process(self, play, d, meth):
        for name, m in d.iteritems():
            getattr(m, meth)(play)

    def __init_cs_teams(self):
        teams = [ self.matchup['home'], self.matchup['away'] ]
        for _, cs in self.cum_stats.items():
            cs.initialize_teams(teams)
  