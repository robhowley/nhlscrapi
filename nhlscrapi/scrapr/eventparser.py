
# annoying boilerplate
# get access to other sub folders
import sys
sys.path.append('../')

from nhlscrapi.games.events import EventType as ET, EventFactory as EF
from nhlscrapi.scrapr import descparser as dp

__event_type_map =  {
    "SHOT": __shot_type,
    "SHOT (!)": __shot_type,
    "SHOT (*)": __shot_type,
    "BLOCK": lambda **kwargs: ET.Block,
    "BLOCKED SHOT": lambda **kwargs: ET.Block
    "MISS": lambda **kwargs: ET.Miss,
    "MISSED SHOT": lambda **kwargs: ET.Miss,
    "GOAL": lambda **kwargs: ET.Goal,
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
    "PEND": lambda **kwargs: ET.End,
    "GEND": lambda **kwargs: ET.End,
    "SOC": lambda **kwargs: ET.End
  }[event_str])


def __shot_type(**kwargs):
  skater_ct = kwargs['skater_ct'] if 'skater_ct' in kwargs else 12
  period = kwargs['period'] if 'period' in kwargs else 1
  
  if skater_ct > 2:
    return ET.Shot
  elif period < 5:
    return EventType.PenaltyShot
  else:
    return EventType.ShoutOutAtt
    

def event_type_mapper(event_str, **kwargs):
  return EF.Create(__event_type_map[event_str](**kwargs))
      
      
def parse_event_desc(event, season = 2008):
  if event.event_type == EventType.Shot and season >= 2008:
    dp.parse_shot_desc_08(event)
  elif event.event_type == EventType.Goal and season >= 2008:
    dp.parse_goal_desc_08(event)
  elif event.event_type == EventType.Miss and season >= 2008:
    dp.parse_miss_08(event)
  elif event.event_type == EventType.FaceOff and season >= 2008:
    dp.parse_faceoff_08(event)
  elif event.event_type == EventType.Hit and season >= 2008:
    dp.parse_hit_08(event)
  elif event.event_type == EventType.Block and season >= 2008:
    dp.parse_block_08(event)
  elif event.event_type == EventType.Takeaway and season >= 2008:
    dp.parse_takeaway_08(event)
  elif event.event_type == EventType.Giveaway and season >= 2008:
    dp.parse_giveaway_08(event)
  else:
    dp.default_desc_parser(event)
