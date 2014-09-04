
from nhlscrapi._tools import exclude_from as ex_junk

def __get_num(s):
  s = s.replace('#', '').strip()
  return int(s) if s.isdigit() else -1
      
def __num_name(s):
  s = s.split(' ')
  if len(s) > 1:
    num = __get_num(s[0])
    name = ' '.join(si.strip() for si in s[1:])
  else:
    num = __get_num(s) if '#' in s else -1
    name = s if num == -1 else ''
        
  return num, name
    
def __make_dict(o):
  d = { }
  for oi in o:
    num, name = __num_name(oi)
    if num in d:
      num = max(d.keys())+1
        
    d[num] = name
        
  return d


def __format_out(refs, lines):
  offs = { 'refs': { }, 'linesman': { } }
  if refs:
    offs['refs'] = __make_dict(refs)
  
  if lines:
    offs['linesman'] = __make_dict(lines)
  
  return offs



# layout of officials seasons <= 2009
def official_parser_pre_09(lx_doc):
  off_row = lx_doc.xpath('//td[contains(text(),"Referee")]')[0].xpath('..')[0]
  
  refs = ex_junk(off_row[1].xpath('.//text()'))
  lines = ex_junk(off_row[3].xpath('.//text()'))
    
  return __format_out(refs, lines)



# layout of officials > 2009
# this needs to be better. can dig deeper into the html to separate tables
# in order to correctly parse the current ambiguity between
# 1 ref, 2 linesman vs 2 refs, 1 linesman
def official_parser_10(lx_doc):
  off_table = lx_doc.xpath('//td[contains(text(),"Referee")]')[0].xpath('../..')[0]
  
  offs = ex_junk(off_table[1].xpath('.//text()'), ['\n','\r'])
  
  if len(offs) == 4:
    return __format_out(offs[:2], offs[2:])
  else:
    return __format_out(offs[:1], offs[1:])



def official_parser_mapper(season):
  if season <= 2009:
    return official_parser_pre_09
  else:
    return official_parser_10

