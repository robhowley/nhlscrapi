
import string
from nhlscrapi.scrapr.teamnameparser import team_abbr_parser
    
# default parser does nothing
def default_desc_parser(event):
  pass

#############################
##
## helper funcs
##
#############################
def rem_char(s, c):
  return s.translate(string.maketrans("",""), c)
  
# get int distance from 'num ft.'
def get_ft(s, def_dist = -1):
  sd = s.split(" ")[0]
  
  return int(sd) if sd.isdigit() else def_dist
  
  
def team_num_name(s):
  tnn = s.split(" ")
  tnn[1] = rem_char(tnn[1], "#")
  tnn[1] = int(tnn[1]) if tnn[1].isdigit() else -1
  
  return {
    "team": team_abbr_parser(tnn[0]),
    "num": tnn[1],
    "name": str(tnn[2] + (tnn[3] if len(tnn) > 3 else ""))  # two word names
  }


def split_and_strip(s, by):
  return [si.strip() for si in s.split(by)]






#############################
##
## parse a shot - '08 format
##
#############################
# NYR ONGOAL - #6 STRALMAN, Slap, Off. Zone, 65 ft.
# shot type might have - in it (wrap-around)
def parse_shot_desc_08(event):
    
  # split to get s[0] team - shooter, s[1] shot type, s[2] zone, s[3] distance
  s = split_and_strip(event.desc, ",")
  
  # split to get team
  st = split_and_strip(s[0], " - ")
  st[0] = rem_char(st[0].split(" ")[0].strip(), ".")
  
  # s[0] in form (#)num name; split by space to get num
  event.shooter = team_num_name(" ".join(st))
  
  # s[1] ' shottype '
  event.shot_type = s[1].strip() if len(s) > 1 else ""
  
  # s[2] has zone ' Off. Zone' or ' Def. Zone'
  event.zone = s[2].strip() if len(s) > 2 else ""
  
  # s[3] distance 'num ft.'
  event.dist = get_ft(s[3]) if len(s) > 3 else -1
  
  
  
#############################
##
## parse a goal - '08 format
##
#############################
# NYR #13 CARCILLO(4), Wrist, Off. Zone, 11 ft. Assists: #15 DORSETT(4); #22 BOYLE(12)
def parse_goal_desc_08(event):
  s = event.desc.split(":")
  
  # assists dictionary = { number, [ name, season total ] }
  a_d = { }
  if len(s) > 1:
    # assists by
    a = [si.strip() for si in s[1].split(";") if si.strip() != ""]
    for ai in a:
      a_l = assist_from(ai)
      a_d[a_l[0]] = a_l[1:3]
      
  event.assists = a_d
  
  s = s[0].split(",")
  s = [e.strip() for e in s if e not in ["Assists", "Assist", "A"]]
  
  # base case
  if len(s) > 3:
    event.shot_type = s[1]
    event.zone = s[2]
    event.dist = get_ft(s[3])
  else:
    # this is really ugly
    try:
      event.dist = get_ft(s[-1])
      if 'zone' in s[-2].lower():
        event.zone = s[-2]
      else:
        event.shot_type = s[-2]
    except:
      if 'zone' in s[-1].lower():
        event.zone = s[-2]
      else:
        event.shot_type = s[-2]
        
  scorer = s[0].split(" ")
  
  # account for two word last names
  if len(scorer) == 4:
    scorer[2] = scorer[2] + " " + scorer[3]
  
  num_str = rem_char(scorer[1], '#')
  pl_tot = [e.strip() for e in scorer[2].split("(")]
  
  event.shooter = {
    'team': team_abbr_parser(scorer[0]),
    'num': int(num_str) if num_str.isdigit() else -1,
    'name': pl_tot[0]
  }
  
  pl_tot[1] = rem_char(pl_tot[1], '()')
  event.shooter_seas_tot = int(pl_tot[1]) if pl_tot[1].isdigit() else -1
    
def assist_from(a):
  pl = a.strip().split(" ")
  num_str = rem_char(pl[0], '#')
  
  r = []
  r.append(int(num_str) if num_str.isdigit() else -1)
  r.extend([p.strip() for p in pl[1].split("(") ])
  if len(r) == 3:
    r[2] = rem_char(r[2], '()')
    
  return r
  
  


#############################
##
## parse a miss - '08 format
##
#############################
# NYR #18 STAAL, Snap, Wide of Net, Off. Zone, 63 ft.
def parse_miss_08(event):
  
  s = split_and_strip(event.desc, ",")
  
  event.shooter = team_num_name(s[0])
  event.shot_type = s[1]
  event.shot_miss_desc = s[2]
  event.zone = s[3]
  
  event.dist = get_ft(s[4])
  
  
  
#############################
##
## parse faceoff - '08 format
##
#############################
# VAN won Off. Zone - NYR #19 RICHARDS vs VAN #22 SEDIN
def parse_faceoff_08(event):
  s = split_and_strip(event.desc, " - ")
  
  w_loc = split_and_strip(s[0], "won")
  event.winner = w_loc[0]
  event.zone = w_loc[1]
  
  vs = s[1].split("vs")
  tnn = team_num_name(vs[0].strip())
  try:
    tnn2 = team_num_name(vs[1].strip())
    event.head_to_head = [ tnn, tnn2 ]
  except:
    print vs



#############################
##
## parse hit - '08 format
##
#############################
# VAN #3 BIEKSA HIT NYR #21 STEPAN, Def. Zone
def parse_hit_08(event):
  s = split_and_strip(event.desc, " HIT ")
  
  event.hit_by = team_num_name(s[0])
  event.team = event.hit_by['team']
  
  p_z = s[1].split(",")
  event.player_hit = team_num_name(p_z[0])
  
  event.zone = p_z[1].strip()
  
  
  

#############################
##
## parse blocked shot - '08 format
##
#############################
# VAN #14 BURROWS BLOCKED BY NYR #27 MCDONAGH, Snap, Def. Zone
def parse_block_08(event):
  s = split_and_strip(event.desc, "BLOCKED BY")
  
  event.shooter = team_num_name(s[0])
  
  s = split_and_strip(s[1], ",")
  event.blocked_by = team_num_name(s[0])
  
  event.shot_type = s[1]
  event.zone = s[2]
  
  

#############################
##
## parse takeaway - '08 format
##
#############################
# NYR TAKEAWAY - #27 MCDONAGH, Def. Zone
def parse_takeaway_08(event):
  s = split_and_strip(event.desc, " - ")
  
  s[0] = s[0].replace('?', ' ')
  event.team = team_abbr_parser(s[0].split(" ")[0].strip())
  
  s = split_and_strip(s[1], ",")
  tnn = team_num_name(str('team ' + s[0]))
  event.player_num = tnn["num"]
  event.player_name = tnn["name"]
  event.zone = s[1]
    
  
  

#############################
##
## parse giveaway - '08 format
## same form as takeaway
##
#############################
# NYR GIVEAWAY - #21 STEPAN, Def. Zone
def parse_giveaway_08(event):
  parse_takeaway_08(event)
  
  
  
  
  
#############################
##
## parse shootout
##
#############################
def parse_shootout(event):
  s = split_and_strip(event.desc, ',')
  
  d_str = s[-1].split(' ')[0]
  event.dist = int(d_str) if d_str.isdigit() else 0
  
  event.shot_type = s[1]
  
  tnn = split_and_strip(s[0], ' ')
  if len(tnn) == 3:
    event.shooter = team_num_name(' '.join(tnn))
  elif len(tnn) == 5:
    event.shooter = team_num_name(' '.join([tnn[0], tnn[3], tnn[4]]))