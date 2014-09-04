
# annoying boilerplate
# get access to other sub folders
import sys
sys.path.append('..')

from functools import wraps
from abc import ABCMeta, abstractmethod

class RepScrWrap(object):
  """Lazy matchup reader base. Reports can be read in pieces. Only need to read matchup on read of first part."""
  
  @staticmethod
  def read_banner(scrapr):
    def wrapper(f):
      @wraps(f)
      def wrapped(self, *f_args, **f_kwargs):
        if not self.__have_matchup:
          attr = getattr(self, scrapr)
          self.matchup = attr.parse_matchup()
          self.__have_matchup = True
        return f(self, *f_args, **f_kwargs)
      return wrapped
    return wrapper
    
  @staticmethod
  def lazy_load(scrapr, loader_name):
    l = '.'.join([scrapr, loader_name])
    def wrapper(f):
      @wraps(f)
      def wrapped(self, *f_args, **f_kwargs):
        already_loaded = self.__lazy.setdefault(l, False)
        
        if not already_loaded:
          attr = getattr(self, scrapr)
          getattr(attr, loader_name)()
          self.__lazy[l] = True
          
        return f(self, *f_args, **f_kwargs)
      return wrapped
    return wrapper
  
  def __init__(self, game_key):
    self.__have_matchup = False
    # for decorated properties that share a loader
    self.__lazy = { }
    
    self.game_key = game_key
    """Game key identifier"""
    
    self.matchup = { }
    """Matchup format: { 'home': '', 'away': '', 'final': { 'home': 0, 'away': 0 } }"""
  
  
  def load_all(self):
    for k,v in self.__lazy.iteritems():
      attr = getattr(self, k)
      getattr(attr, v)()
      self.__lazy[k] = True