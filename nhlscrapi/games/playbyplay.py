
from nhlscrapi._tools import build_enum

from nhlscrapi.scrapr.rtss import RTSS
from nhlscrapi.games.repscrwrap import RepScrWrap
  
Strength = build_enum('Even', 'PP', 'SH')
"""Enum indicating play strength."""

class Play(object):
    """Contains base level of state info about a given play."""
    def __init__(self,
            play_num=0, period=0, strength=Strength.Even, time={ "min": 20, "sec": 0 },
            vis_on_ice = { }, home_on_ice = { }, event=None):
                
        self.play_num = play_num
        """Number of player who made the play"""
        
        self.period = period
        """Current period"""
        
        self.strength = strength
        """Enum of type :py:class:`.Strength` indicating either even strength, shorthanded, or power play"""
        
        self.time = time
        """Time remaining in the period"""
        
        self.vis_on_ice = vis_on_ice
        """Visiting skaters on the ice. ``{ num: [position, name] }``"""
        
        self.home_on_ice = home_on_ice
        """Home skaters on the ice. ``{ num: [position, name] }``"""
        
        self.event = event
        """
        An object that inherits from :py:class:`.Event` that contains other specifics related to
        the given type of play
        """

class PlayByPlay(RepScrWrap):
    """
    Aggregator of :py:class:`.Play` objects that maintains the play-by-play data for a given game. Allows for
    custom stats of type :py:class:`.AccumulateStats` to be computed for the game.
    
    :Example:
    
    .. code:: python
    
        from nhlscrapi.games.game import GameKey
        from nhlscrapi.games.cumstats import ShotCt
        from nhlscrapi.games.playbyplay import PlayByPlay
        
        # define the game of interest and a stat accumulator
        pbp = PlayByPlay(
            game_key=GameKey(2015, 3, 224),
            cum_stats={ 'ShotCount': ShotCt() }
        )
        
        # compute and print results
        shot_cts = pbp.compute_stats()['ShotCount']
        print('Final Score:\t{}'.format(shot_cts.total))
    """
    
    def __init__(self, game_key, cum_stats = {}, init_cs_teams=True):
        super(PlayByPlay, self).__init__(game_key, RTSS(game_key))
        
        self.cum_stats = cum_stats
        """Dictionary of :py:class:`.AccumulateStats` to be computed"""
        
        self.init_cs_teams = init_cs_teams
        """Boolean, (default) True if the :py:class:`.AccumulateStats` objects should have team names initialized."""
        
        self.__have_stats = False
        self.__wrapped_plays = []
    
    # doesn't need to be dispatched
    # this is managed by compute_stats
    @property
    def plays(self):
        """List of :py:class:`.Play` objects."""
        self.compute_stats()
        return self.__wrapped_plays
        
    def compute_stats(self):
        """
        Compute the stats defined in ``self.cum_stats``.
        
        :returns: collection of all computed :py:class:`.AccumulateStats`
        :rtype: dict
        """
        if not self.__have_stats:
            if self.init_cs_teams and self.cum_stats:
                self.__init_cs_teams()
            
            for play in self._rep_reader.parse_plays_stream():
                p = Play(**play)
                self.__wrapped_plays.append(p)
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
  