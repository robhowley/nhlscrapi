
from nhlscrapi.constants import TEAMS_BY_ABBR as ABB

__abbr_alts = {
  'LAK': 'LA'
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
  # give proper capitalization, translate to expected team name
  # WASHINGTON CAPITALS -> Washington Capitals
  # ST. LOUIS BLUES -> St Louis Blues
  ns = ' '.join(s[:1].upper() + s[1:] for s in name.lower().replace('.','').split(' '))
  
  try:
    return ABB.keys()[ABB.values().index(ns)] #Reverse lookup, by value.
  except:
    #print 'UNKNOWN TEAM NAME: %s' % name
    pass
  
  return name