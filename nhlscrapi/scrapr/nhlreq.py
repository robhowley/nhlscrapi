

from urllib2 import urlopen
from urllib2 import Request
from urllib2 import URLError

from datetime import datetime as dt

class NHLCn(object):
  
  __domain = 'http://www.nhl.com/'
  
  def __init__(self):
    self.html_src = None
    self.req_err = None
    self.req_time = 0
  
  def rtss(self, game_key):
    seas, gt, num = game_key.to_tuple()
    url = [ self.__domain, "scores/htmlreports/", str(seas-1), str(seas),
      "/PL0", str(gt), ("%04i" % (num)), ".HTM" ]
    print ''.join(url)
    return self.__open(''.join(url))
  
  def __open(self, url):
    req = Request(url, headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'})
    
    start = dt.now()
    
    req = None
    try:
      req = urlopen(url)
      self.html_src = req.read()
    except Exception as e:
      self.req_err = e
    else:
      if self.req_err is not None:
        req.close()
    
    self.req_time = dt.now() - start
      
    return self.html_src

