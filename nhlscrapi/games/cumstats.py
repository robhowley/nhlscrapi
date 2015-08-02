
from abc import ABCMeta, abstractmethod

from nhlscrapi.games import events as EV
from nhlscrapi.games.events import EventFactory as EF

from nhlscrapi.games.playbyplay import Strength as St

# base class for accumulators
class AccumulateStats(object):
    """
    Base class for accumulator classes. These classes keep tallies of specified events and
    are updated each time a play from :py:class:`.PlayByPlay` is processed. Examples
    include :py:class:`.ShotCt` and :py:class:`.Score`. This class is not intended to be
    used directly.
    """
    __metaclass__ = ABCMeta
  
    def __init__(self):
        self.total = { }
        self.teams = []
    
    def initialize_teams(self, teams):
        self.teams = teams
        self.total = { t: 0 for t in teams }
    
    @abstractmethod
    def update(self, play):
        """
        Update the accumulator with the current play
        
        :returns: new tally, ``{ 'period': per, 'time': clock, 'team': cumul, 'play': play }``
        """
        pass


class TeamIncrementor(AccumulateStats):
    """
    Accumulator base class for team vs team stats such as score, shot count et c.
    
    :param get_team: function, takes a play and returns the team associated with it
    :param count_play: function, takes a play and returns True if it is a tally for the given accumulator's definition.
    """
    __metaclass__ = ABCMeta
  
    def __init__(self, get_team=None, count_play=None):
        super(TeamIncrementor, self).__init__()
        self.tally = []
        """List of plays that lead to tallies, i.e. increments of the stat accumulator. E.g. a goal or shot."""
        
        self._get_team = get_team
        self._count_play = count_play
    
    def update(self, play):
        """
        Update the accumulator with the current play
        
        :returns: new tally
        :rtype: dict, ``{ 'period': per, 'time': clock, 'team': cumul, 'play': play }``
        """
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
                new_tally['play'] = play
            except:
                new_tally = {
                    'period': play.period,
                    'time': play.time,
                    team: 1,
                    'play': play
                }
      
            self.tally.append(new_tally)
      
        return new_tally
      

class ShotEventTallyBase(TeamIncrementor):
    """Base class for all shot attempt based events"""
    def __init__(self, count_play):
        super(ShotEventTallyBase, self).__init__(
            get_team=lambda play: play.event.shooter['team'],
            count_play=count_play
        )
            
      
class ShotCt(ShotEventTallyBase):
    """
    Tallies shots on goal for each team. Increments if
    
      * the play event inherits from :py:class:`.Shot`
    
    """
    def __init__(self):
        super(ShotCt, self).__init__(
            count_play=lambda play: isinstance(play.event, EV.Shot)
        )


class EvenStShotCt(ShotEventTallyBase):
    """
    Tallies even strength shots on goal for each team. Increments if
    
      * the play event inherits from :py:class:`.Shot`
      * play happened at even strength
    
    """
    def __init__(self):
        super(EvenStShotCt, self).__init__(
            count_play=lambda play: isinstance(play.event, EV.Shot) and play.strength == St.Even
        )

    
class ShotAttemptCt(ShotEventTallyBase):
    """
    Tallies even strength shots on goal for each team. Increments if
    
      * the play event inherits from :py:class:`.ShotAttempt`
    
    """
    def __init__(self):
        super(ShotAttemptCt, self).__init__(
            count_play=lambda play: isinstance(play.event, EV.ShotAttempt)
        )

    
class EvenStShotAttCt(ShotEventTallyBase):
    """
    Tallies even strength shots on goal for each team. Increments if
    
      * the play event inherits from :py:class:`.ShotAttempt`
      * play happened at even strength
    
    """
    def __init__(self):
        super(EvenStShotAttCt, self).__init__(
            count_play=lambda play: isinstance(play.event, EV.ShotAttempt) and play.strength == St.Even
        )
    
    
class Corsi(EvenStShotAttCt):
    """
    Tallies even strength shots on goal for each team. Increments if
    
      * the play event inherits from :py:class:`.Shot`
      * play happened at even strength
    
    Defined more for convention/nostalgia. Same as :py:class:`.EvenStShotAttCt`
    """
    def __init__(self):
        super(Corsi, self).__init__()
    
    def share(self):
        """
        The Cori-share (% of shot attempts) for each team
        
        :returns: dict, ``{ 'home_name': %, 'away_name': % }``
        """
        tot = sum(self.total.values())
        return { k: v/float(tot) for k,v in self.total.iteritems() }


class ShootOut(ShotEventTallyBase):
    """
    Tallies shootout goals. Increments if
    
      * the play event inherits from :py:class:`.ShootOutGoal`
      
    """
    def __init__(self):
        super(ShootOut, self).__init__(
            count_play=lambda play: isinstance(play.event, EV.ShootOutGoal)
        )
    

# doesn't fit nicely into ShotEventTallyBase framework
# due to dual source nature, it doesn't quite fit
class Score(ShotEventTallyBase):
    """Tallies if a goal is scored. Also tracks shootout goals. Increments if
    
      * the play event inherits from :py:class:`.Goal`
      * the play event inherits from :py:class:`.ShootOutGoal`
    
    """
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
        
    def initialize_teams(self, teams):
        super(Score, self).initialize_teams(teams)
        self.shootout.initialize_teams(teams)

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
            t1wins = 1 if self.shootout.total[t1] > self.shootout.total[t2] else 0
            self.total[t1] += t1wins
            self.total[t2] += 1-t1wins
    
    
class Fenwick(ShotEventTallyBase):
    """Tallies if a goal is scored. Also tracks shootout goals. Increments if
    
      * the play event inherits from :py:class:`.ShotAttempt`
      * the play event does not inherit from :py:class:`.Block`
      * play happened at even strength
    
    """
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
        
    def initialize_teams(self, teams):
        super(Fenwick, self).initialize_teams(teams)
        self.score.initialize_teams(teams)
    
    def share(self):
        """
        :returns: The Fenwick-share (% of unblocked even strength shot attempts) for each team
        :rtype: dict, ``{ 'home_name': %, 'away_name': % }``
        """
        tot = sum(self.total.values())
        return { k: v/float(tot) for k,v in self.total.iteritems() }