

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


