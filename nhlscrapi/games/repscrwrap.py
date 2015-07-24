
from functools import wraps
from abc import ABCMeta, abstractmethod

def dispatch_loader(scrapr, loader_name):
    l = '.'.join([scrapr, loader_name])
    def wrapper(f):
        @wraps(f)
        def wrapped(self, *f_args, **f_kwargs):
            if not hasattr(self, '_loaded'):
                self._loaded = { }
                
            already_loaded = self._loaded.setdefault(l, False)
            if not already_loaded:
                attr = getattr(self, scrapr)
                self._loaded[l] = getattr(attr, loader_name)() is not None
            return f(self, *f_args, **f_kwargs)
        return wrapped
    return wrapper
        
        
class RepScrWrap(object):
    """Lazy matchup reader base. Reports can be read in pieces. Only need to read matchup on read of first part. Serves
    as the base class for all wrappers of report scrapers. """

    def __init__(self, game_key, rep_reader):
        self.__have_matchup = False
        
        self.game_key = game_key
        """Game key identifier"""
        
        self._rep_reader = rep_reader
    
    
    @property
    @dispatch_loader('_rep_reader', 'parse_matchup')
    def matchup(self):
        return self._rep_reader.matchup
        
        
    def load_all(self):
        for k,v in self._lazy.iteritems():
            if not v:
                attr = getattr(self, k)()
                self.__lazy[k] = True
