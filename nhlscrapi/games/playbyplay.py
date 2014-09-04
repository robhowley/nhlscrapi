
# annoying boilerplate
# get access to other sub folders
import sys
sys.path.append('..')

from nhlscrapi.scrapr.rtss import RTSS
from nhlscrapi.games.repscrwrap import RepScrWrap
  

class PlayByPlay(RepScrWrap):
  def __init__(self, game_key, extractors = {}, cum_stats = {}):
    super(PlayByPlay, self).__init__(game_key)
    
    self._rtss = RTSS(game_key)

    self.extractors = extractors
    self.cum_stats = cum_stats
  
    self.__have_stats = False
  
  @RepScrWrap.read_banner('_rtss')
  @RepScrWrap.lazy_load('_rtss', 'parse_plays')
  def plays(self):
    if not self.__have_stats:
      self.compute_stats()
      self.__have_stats = True
  
    return self._rtss.plays
  
  @RepScrWrap.read_banner('_rtss')
  @RepScrWrap.lazy_load('_rtss', 'parse_plays_stream')
  def compute_stats(self):
    if not self.__have_stats:
      for play in self._rtss.parse_plays_stream():
        self.__process(play, self.extractors, 'extract')
        self.__process(play, self.cum_stats, 'update')
      self.__have_stats = True
    
    return self.plays
    
  def __process(self, play, d, meth):
    for name, m in d.iteritems():
      getattr(m, meth)(play)
      
  