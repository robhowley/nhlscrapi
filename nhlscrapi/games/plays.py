
# annoying boilerplate
# get access to other sub folders
import sys
sys.path.append('..')

from nhlscrapi._tools import build_enum
  
Strength = build_enum('Even', 'PP')

class Play(object):
  def __init__(self):
    self.play_num = 0
    self.period = 0
    self.strength = Strength.Even
    self.time = { "min": 20, "sec": 0 }
    self.vis_on_ice = { }
    self.home_on_ice = { }
    self.event = 0