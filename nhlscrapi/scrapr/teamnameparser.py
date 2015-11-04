
from nhlscrapi.constants import TEAMS_BY_ABBR as ABB

__abbr_alts = {
  'LAK': 'LA',
  'NJD': 'NJ',
  'SJS': 'SJ',
  'TBL': 'TB'
}

def team_abbr_parser(abr):
  abr = abr.replace('.','')
  
  # keep abr if already in good shape
  if abr in ABB:
    return abr
    
  if abr in __abbr_alts:
    return __abbr_alts[abr]
    
  #print 'UNKNOWN ABBREVIATION: %s' % abr
  return abr


def team_name_parser(name):
  
  # give proper capitalization
  ns = ' '.join(s[:1].upper() + s[1:] for s in name.lower().split(' '))
  
  try:
    return ABB.keys()[ABB.values().index(ns)]
  except:
    #print 'UNKNOWN TEAM NAME: %s' % name
    pass
  
  return name
  
  
