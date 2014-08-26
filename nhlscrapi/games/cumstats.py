
from abc import ABCMeta, abstractmethod

from nhlscrapi.games import events as EV
from nhlscrapi.games.events import EventFactory as EF

from nhlscrapi.games.plays import Strength as St

# base class for accumulators
class AccumulateStats(object):
  __metaclass__ = ABCMeta
  
  def __init__(self):
    self.total = { }
    
  @abstractmethod
  def update(self, play):
    pass



class TeamIncrementor(AccumulateStats):
  
  __metaclass__ = ABCMeta
  
  def __init__(self):
    super(TeamIncrementor, self).__init__()
    self.tally = []
    self.teams = []
  
  @abstractmethod
  def _get_team(self, play):
    pass
  
  @abstractmethod
  def _count_play(self, play):
    pass
    
  def update(self, play):
    #if any(isinstance(play.event, te) for te in self.trigger_event_types):
    if self._count_play(play):
      # the team who made the play / triggered the event
    
      team = self._get_team(play)
      if team == '':
        print play.event
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
    super(ShotCt, self).__init__()

  def _get_team(self, play):
    return play.event.shooter['team']

  def _count_play(self, play):
    return isinstance(play.event, EV.Shot)


    
class ShotAttemptCt(TeamIncrementor):
  def __init__(self):
    super(ShotAttemptCt, self).__init__()
    
  def _get_team(self, play):
    return play.event.shooter['team']

  def _count_play(self, play):
    return isinstance(play.event, EV.ShotAttempt)
    

    
class EvStrShotAttCt(TeamIncrementor):
  def __init__(self):
    super(EvStrShotAttCt, self).__init__()
    
  def _get_team(self, play):
    return play.event.shooter['team']

  def _count_play(self, play):
    return isinstance(play.event, EV.ShotAttempt) and play.strength == St.Even
    
    
class Corsi(ShotAttemptCt):
  def __init__(self):
    super(Corsi, self).__init__()
    
  def _count_play(self, play):
    return isinstance(play.event, EV.ShotAttempt) and play.strength == St.Even
    
  def share(self):
    tot = sum(self.total.values())
    return { k: v/float(tot) for k,v in self.total.iteritems() }


# doesn't include shootout, can't get final as an incrementor
# need to find a workaround
class Score(TeamIncrementor):
  def __init__(self):
    super(Score, self).__init__()

  def _get_team(self, play):
    return play.event.shooter['team']

  def _count_play(self, play):
    return isinstance(play.event, EV.Goal) and play.period < 5
    
    
class Fenwick(ShotAttemptCt):
  def __init__(self):
    super(Fenwick, self).__init__()
    self.score = Score()
    
  def _count_play(self, play):
    
    # if not the right event type, don't bother checking 'close'
    is_p_type = isinstance(play.event, EV.ShotAttempt) \
      and not isinstance(play.event, EV.Block) \
      and play.strength == St.Even
    
    close = False
    if is_p_type:
      scr = 0
      if len(self.score.teams):
        t = self.score.teams[0]
        scr = self.score.total[t]
      if len(self.score.teams) > 1:
        t = self.score.teams[1]
        scr -= self.score.total[t]
      
      close = (scr <= 2 and play.period < 3) or (scr <= 1 and play.period >= 3)
    
    return is_p_type and close
  
  def update(self, play):
    self.score.update(play)
    super(Fenwick, self).update(play)
    
  def share(self):
    tot = sum(self.total.values())
    return { k: v/float(tot) for k,v in self.total.iteritems() }