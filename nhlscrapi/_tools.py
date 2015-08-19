
import re
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
    reverse = dict((value, key) for key, value in enums.items())
    enums['Name'] = reverse
    return type('Enum', (), enums)


def exclude_from(l, containing = [], equal_to = []):
    """Exclude elements in list l containing any elements from list ex.
    Example:
        >>> l = ['bob', 'r', 'rob\r', '\r\nrobert']
        >>> containing = ['\n', '\r']
        >>> equal_to = ['r']
        >>> exclude_from(l, containing, equal_to)
        ['bob']
    """
      
    cont = lambda li: any(c in li for c in containing)
    eq = lambda li: any(e == li for e in equal_to)
    return [li for li in l if not (cont(li) or eq(li))]
  
  
def to_int(s, default=-1):
    mult = 1
    if s[0] in ['-','+']:
        mult = -1 if '-' in s else 1
        s = s[1:]
    return mult*int(s) if s.isdigit() else 0 if s == '00' else default

  
def split_time(t):
    ti = t.split(':')
    return { 'min': to_int(ti[0]), 'sec': to_int(ti[1]) }
    
    
def re_comp_num_pos_name():
    """
    Compiles the regex pattern that extracts the pattern (num) (position) (last), (first)
    
    Example:
        s = '21 C Stepan, Derek'
        reg = re_comp_num_pos_name()
        num, pos, last, first = reg.findall(s)[0]
    
    :return: compiled regex
    """
    return re.compile(r'(\d+)\s*(\w+)\s*([^\,]+)[\W]+(\w+)')  # (num) (position) (last), (first)