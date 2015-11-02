

from nhlscrapi.games.events import EventType as ET, EventFactory as EF
from nhlscrapi.scrapr import descparser as dp


def __shot_type(**kwargs):
  skater_ct = kwargs['skater_ct'] if 'skater_ct' in kwargs else 12
  period = kwargs['period'] if 'period' in kwargs else 1
  
  if period < 5:
    return ET.Shot
#  elif period < 5:
#    return ET.PenaltyShot
  else:
    return ET.ShootOutAtt

def __goal_type(**kwargs):
  skater_ct = kwargs['skater_ct'] if 'skater_ct' in kwargs else 12
  period = kwargs['period'] if 'period' in kwargs else 1
  gt = kwargs['game_type']
  
  if skater_ct <= 7 and period > 4 and gt < 3:
    return ET.ShootOutGoal
  else:
    return ET.Goal

def event_type_mapper(event_str, **kwargs):
  event_type_map =  {
    "SHOT": __shot_type,
    "SHOT (!)": __shot_type,
    "SHOT (*)": __shot_type,
    "BLOCK": lambda **kwargs: ET.Block,
    "BLOCKED SHOT": lambda **kwargs: ET.Block,
    "MISS": lambda **kwargs: ET.Miss,
    "MISSED SHOT": lambda **kwargs: ET.Miss,
    "GOAL": __goal_type,
    "HIT": lambda **kwargs: ET.Hit,
    "HIT (!)": lambda **kwargs: ET.Hit,
    "HIT (*)": lambda **kwargs: ET.Hit,
    "FAC": lambda **kwargs: ET.FaceOff,
    "FACE-OFF": lambda **kwargs: ET.FaceOff,
    "GIVE": lambda **kwargs: ET.Giveaway,
    "GIVEAWAY": lambda **kwargs: ET.Giveaway,
    "TAKE": lambda **kwargs: ET.Takeaway,
    "TAKEAWAY": lambda **kwargs: ET.Takeaway,
    "PENL": lambda **kwargs: ET.Penalty,
    "PENALTY": lambda **kwargs: ET.Penalty,
    "STOP": lambda **kwargs: ET.Stoppage,
    "STOPPAGE": lambda **kwargs: ET.Stoppage,
    "PEND": lambda **kwargs: ET.PeriodEnd,
    "GEND": lambda **kwargs: ET.GameEnd,
    "SOC": lambda **kwargs: ET.ShootOutEnd
  }
  
  e_type = event_type_map[event_str](**kwargs) if event_str in event_type_map else ET.Event
  
  return EF.Create(e_type)
      
      
def parse_event_desc(event, season = 2008):
    
    if event.event_type == ET.Shot and season >= 2008:
        dp.parse_shot_desc_08(event)
#    elif event.event_type == ET.PenaltyShot:
#        dp.parse_penalty_shot_desc_08(event)
    elif event.event_type == ET.Goal and season >= 2008:
        dp.parse_goal_desc_08(event)
    elif event.event_type == ET.Miss and season >= 2008:
        dp.parse_miss_08(event)
    elif event.event_type == ET.FaceOff and season >= 2008:
        dp.parse_faceoff_08(event)
    elif event.event_type == ET.Hit and season >= 2008:
        dp.parse_hit_08(event)
    elif event.event_type == ET.Block and season >= 2008:
        dp.parse_block_08(event)
    elif event.event_type == ET.Takeaway and season >= 2008:
        dp.parse_takeaway_08(event)
    elif event.event_type == ET.Giveaway and season >= 2008:
        dp.parse_giveaway_08(event)
    elif event.event_type == ET.ShootOutGoal:
        dp.parse_shootout(event)
    else:
        dp.default_desc_parser(event)
