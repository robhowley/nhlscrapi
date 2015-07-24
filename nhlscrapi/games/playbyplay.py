

from nhlscrapi.scrapr.rtss import RTSS
from nhlscrapi.games.repscrwrap import RepScrWrap
  

class PlayByPlay(RepScrWrap):
    def __init__(self, game_key, extractors = {}, cum_stats = {}):
        super(PlayByPlay, self).__init__(game_key, RTSS(game_key))
        
        #    self._rtss = RTSS(game_key)
        self.extractors = extractors
        self.cum_stats = cum_stats
        self.__have_stats = False
        
    
    # doesn't need to be dispatched
    # this is managed by compute_stats
    @property
    def plays(self):
        self.compute_stats()
        return self._rep_reader.plays
        
        
    def compute_stats(self):
        if not self.__have_stats:
            for play in self._rep_reader.parse_plays_stream():
                self.__process(play, self.extractors, 'extract')
                self.__process(play, self.cum_stats, 'update')
                self.__have_stats = True
                
        return self.cum_stats
        
        
    def __process(self, play, d, meth):
        for name, m in d.iteritems():
            getattr(m, meth)(play)
      
  