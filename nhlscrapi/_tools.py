

import json

# need to fix this to accommodate recursion depth limit/error
# if not, then go through the pain staking of a class.to_json() structure? ugh
class JSONDataEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
      return json.JSONEncoder.default(self, obj)
    else:
      return obj.__dict__
  
# didn't use built in enum for backwards compat
def build_enum(*sequential, **named):
  enums = dict(zip(sequential, range(len(sequential))), **named)
  reverse = dict((value, key) for key, value in enums.iteritems())
  enums['Name'] = reverse
  return type('Enum', (), enums)



def exclude_from(l, containing = [], equal_to = []):
  """Exclude elements in list l containing any elements from list ex.
  Example:
      >>> l = ['bob', 'r', 'rob\r', '\r\nrobert']
      >>> containing = ['\n', '\r']
      >>> equal_to = ['r']
      >>> exclude_from(l, containing, equal_to)
      ['bob']"""
      
  cont = lambda li: any(c in li for c in containing)
  eq = lambda li: any(e == li for e in equal_to)
  return [li for li in l if not (cont(li) or eq(li))]
  
  
def to_int(s,default=-1):
  return int(s) if s.isdigit() else default