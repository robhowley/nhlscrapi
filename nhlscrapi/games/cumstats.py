
from abc import ABCMeta, abstractmethod

from nhlscrapi.games import events as EV

# base class for accumulators
class AccumulateStats(object):
  __metaclass__ = ABCMeta
  
  def __init__(self):
    self.total = { }
    
  @abstractmethod
  def update(self, play):
    return


class TeamIncrementor(AccumulateStats):
  def __init__(self, trigger_events):
    super(TeamIncrementor, self).__init__()
    self.tally = []
    self.teams = []
    self.trigger_events = trigger_events
    
  def update(self, play):
    if any(isinstance(play.event, te) for te in self.trigger_events):
      # the team who made the play / triggered the event
      team = play.event.team
      
      try:
        self.total[team] += 1
      except:
        self.total[team] = 1
        self.teams.append(team)
        for i in range(len(self.tally)):
          self.tally[i][team] = 0
      
      try:
        new_tally = { k:v for k,v in self.tally[len(self.tally)-1].iteritems() }
        new_tally['period'] = play.period
        new_tally['time'] = play.time
        new_tally[team] += 1
      except:
        new_tally = {
          'period': play.period,
          'time': play.time,
          team: 1
        }
      
      self.tally.append(new_tally)
      
    return
      
      
class ShotCt(TeamIncrementor):
  def __init__(self):
    super(ShotCt, self).__init__([EV.Shot])

class ShotAttemptCt(TeamIncrementor):
  def __init__(self):
    super(ShotAttemptCt, self).__init__([EV.ShotAttempt])
