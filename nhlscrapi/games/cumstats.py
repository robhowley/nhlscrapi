
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
  
    def __init__(self, get_team=None, count_play=None):
        super(TeamIncrementor, self).__init__()
        self.tally = []
        self.teams = []
        self._get_team = get_team
        self._count_play = count_play
    
    def update(self, play):
        new_tally = { }
        #if any(isinstance(play.event, te) for te in self.trigger_event_types):
        if self._count_play(play):
            # the team who made the play / triggered the event
    
            team = self._get_team(play)
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
      
        return new_tally
      

class ShotEventTallyBase(TeamIncrementor):
    def __init__(self, count_play):
        super(ShotEventTallyBase, self).__init__(
            get_team=lambda play: play.event.shooter['team'],
            count_play=count_play
        )
            
      
class ShotCt(ShotEventTallyBase):
    def __init__(self):
        super(ShotCt, self).__init__(
            count_play=lambda play: isinstance(play.event, EV.Shot)
        )
    

class EvenStShotCt(ShotEventTallyBase):
    def __init__(self):
        super(EvenStShotCt, self).__init__(
            count_play=lambda play: isinstance(play.event, EV.Shot) and play.strength == St.Even
        )

    
class ShotAttemptCt(ShotEventTallyBase):
    def __init__(self):
        super(ShotAttemptCt, self).__init__(
            count_play=lambda play: isinstance(play.event, EV.ShotAttempt)
        )

    
class EvenStShotAttCt(ShotEventTallyBase):
    def __init__(self):
        super(EvenStShotAttCt, self).__init__(
            count_play=lambda play: isinstance(play.event, EV.ShotAttempt) and play.strength == St.Even
        )
    
    
class Corsi(EvenStShotAttCt):
    """
    Defined more for convention/nostalgia. Totals are same as EvenStShotAttCt
    """
    def __init__(self):
        super(Corsi, self).__init__()
    
    def share(self):
        tot = sum(self.total.values())
        return { k: v/float(tot) for k,v in self.total.iteritems() }


class ShootOut(ShotEventTallyBase):
    def __init__(self):
        super(ShootOut, self).__init__(
            count_play=lambda play: isinstance(play.event, EV.ShootOutGoal)
        )
    

# doesn't fit nicely into ShotEventTallyBase framework
# due to dual source nature, it doesn't quite fit
class Score(ShotEventTallyBase):
    def __init__(self):
        self.shootout = ShootOut()
        
        def _count_play(self, play):
            if isinstance(play.event, EV.ShootOutEnd):
                self.__set_shootout_winner()
      
            return isinstance(play.event, EV.Goal)
            
        super(Score, self).__init__(
            count_play=lambda play: _count_play(self, play)
        )
        

    def update(self, play):
        self.shootout.update(play)
        super(Score, self).update(play)

    def __set_shootout_winner(self):
        t1 = self.shootout.teams[0]
        if len(self.shootout.teams) == 1:
            try:
                self.total[t1] += 1
            except:
                self.total[t1] = 1
        else:
            t2 = self.shootout.teams[1]
            if len(self.teams) != 2:
                self.teams = [t1, t2]
            t1wins = 1 if self.shootout[t1] > self.shootout[t2] else 0
            self.total[t1] += t1wins
            self.total[t2] += 1-t1wins
    
    
class Fenwick(ShotEventTallyBase):
    def __init__(self):
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
        
        super(Fenwick, self).__init__(
            count_play=lambda play: _count_play(self, play)
        )
        
  
    def update(self, play):
        self.score.update(play)
        super(Fenwick, self).update(play)
    
    def share(self):
        tot = sum(self.total.values())
        return { k: v/float(tot) for k,v in self.total.iteritems() }