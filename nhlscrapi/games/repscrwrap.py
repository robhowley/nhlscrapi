
from functools import wraps
from abc import ABCMeta, abstractmethod

def dispatch_loader(scraper, loader_name):
    """
    Decorator that enforces one time loading for scrapers. The one time loading is applied
    to partial loaders, e.g. only parse and load the home team roster once. This is not
    meant to be used directly.
    
    :param scraper: property name (string) containing an object of type :py:class:`scrapr.ReportLoader`
    :param loader_name: name of method that does the scraping/parsing
    :returns: function wrapper
    """
    l = '.'.join([scraper, loader_name])
    def wrapper(f):
        @wraps(f)
        def wrapped(self, *f_args, **f_kwargs):
            if not hasattr(self, '_loaded'):
                self._loaded = { }
                
            already_loaded = self._loaded.setdefault(l, False)
            if not already_loaded:
                attr = getattr(self, scraper)
                self._loaded[l] = getattr(attr, loader_name)() is not None
            return f(self, *f_args, **f_kwargs)
        return wrapped
    return wrapper
        
        
class RepScrWrap(object):
    """
    Lazy matchup reader base. Reports can be read in pieces. Only need to read matchup on read of first part. Serves
    as the base class for all wrappers of report scrapers.
    
    :param game_key: :py:class:`.GameKey` of the game being loaded
    :param rep_reader: object of type :py:class:`nhlscrapi.scrapr.ReportLoader`
    """

    def __init__(self, game_key, rep_reader):
        self.__have_matchup = False
        
        self.game_key = game_key
        """Game key identifier of type :py:class:`.GameKey`"""
        
        self._rep_reader = rep_reader
    
    
    @property
    @dispatch_loader('_rep_reader', 'parse_matchup')
    def matchup(self):
        """
        Return the game meta information displayed in report banners including team names,
        final score, game date, location, and attendance. Data format is
        
        .. code:: python
        
            {
                'home': home,
                'away': away,
                'final': final,
                'attendance': att,
                'date': date,
                'location': loc
            }
            
        :returns: matchup banner info
        :rtype: dict
        """
        return self._rep_reader.matchup
        
    def load_all(self):
        """
        Loads all parts of the report.
        
        :returns: ``self`` or ``None`` if load fails
        """
        if self._rep_reader.parse():
            return self
        else:
            return None
