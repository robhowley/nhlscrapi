

from nhlscrapi._tools import build_enum


EventType = build_enum('Event', 'ShotAttempt', 'Shot', 'Block', 'Miss', 'Goal',
    'Hit', 'FaceOff', 'Giveaway', 'Takeaway', 'Penalty', 'Stoppage', 'ShootOutAtt',
    'ShootOutGoal', 'PeriodEnd', 'GameEnd', 'ShootOutEnd')
"""Enum indicating event type."""
  
  
class Event(object):
    """Base class for event codes in the RTSS play-by-play reports"""
    def __init__(self, event_type = EventType.Event, desc = ""):
        self.event_type = event_type
        """The :py:class:`.EventType` enum values corresponding to the event."""
        
        self.desc = desc
        """The RTSS description of the play."""
        
        
class ShotAttempt(Event):
    def __init__(self, event_type = EventType.ShotAttempt):
        super(ShotAttempt, self).__init__(event_type)
        self.shooter = { 'team': '', 'name': '', 'num': 0 }
        """Shooter info ``{ 'team': team, 'name': name, 'num': num }``"""
        
        self.shot_type = ""
        """Description of shot, e.g. Wrist Shot, et c"""
        
        self.dist = 0
        """Distance of shot in feet"""
        
        self.is_penalty_shot = False
        """Flag indicating if it was a penalty shot"""
        
        
class Shot(ShotAttempt):
    def __init__(self):
        super(Shot, self).__init__(EventType.Shot)
        
        
class Goal(Shot):
    def __init__(self):
        super(Goal, self).__init__()
        self.event_type = EventType.Goal
        self.assists = []
        
        
class Miss(ShotAttempt):
    def __init__(self):
        super(Miss, self).__init__(EventType.Miss)
        
        
class Block(ShotAttempt):
    def __init__(self):
        super(Block, self).__init__(EventType.Block)
        
        
class Hit(Event):
    def __init__(self):
        super(Hit, self).__init__(EventType.Hit)
        
        
class FaceOff(Event):
    def __init__(self):
        super(FaceOff, self).__init__(EventType.FaceOff)
        
        
class Stoppage(Event):
    def __init__(self, event_type=EventType.Stoppage):
        super(Stoppage, self).__init__(event_type)
        
        
class PeriodEnd(Stoppage):
    def __init__(self):
        super(PeriodEnd, self).__init__(EventType.PeriodEnd)
        
        
class GameEnd(Stoppage):
    def __init__(self):
        super(GameEnd, self).__init__(EventType.GameEnd)
        
        
class ShootOutEnd(Stoppage):
    def __init__(self):
        super(ShootOutEnd, self).__init__(EventType.ShootOutEnd)
        
        
class Penalty(Event):
    def __init__(self):
        super(Penalty, self).__init__(EventType.Penalty)
        
        
class Turnover(Event):
    """Base class for Takeaway and Giveaway events. Not meant to be used directly"""
    class TOType:
        Takeaway = 0
        Giveaway = 1
        
    def __init__(self, to_type = TOType.Takeaway):
        self.to_type = to_type
        if to_type == Turnover.TOType.Giveaway:
            super(Turnover, self).__init__(EventType.Giveaway)
        else:
            super(Turnover, self).__init__(EventType.Takeaway)
            
    @property
    def turnover_type(self):
        return self._turnover_type
        
    @turnover_type.setter
    def turnover_type(self, value):
        if isinstance(value, TOType):
            self._turnover_type = value
        else:
            raise ValueError(str(value) + " is not of type Turnover.TOType")
            
            
class Takeaway(Turnover):
    def __init__(self):
        super(Takeaway, self).__init__(Turnover.TOType.Takeaway)
        
        
class Giveaway(Turnover):
    def __init__(self):
        super(Giveaway, self).__init__(Turnover.TOType.Giveaway)
        
        
# accumulators are based upon inheritance
# shoot outs don't count as a shot attempts
class ShootOutAtt(Event):
    def __init__(self, event_type = EventType.ShootOutAtt):
        super(ShootOutAtt, self).__init__(event_type)
        self.shooter = { 'team': '', 'name': '', 'num': 0 }
        self.shot_type = ""
        self.dist = 0
        
        
class ShootOutGoal(ShootOutAtt):
    def __init__(self):
        super(ShootOutGoal, self).__init__(EventType.ShootOutGoal)
        
        
def _get_class_hierarchy(base):
    l = [base]
    for t in base.__subclasses__():
        grandchildren = t.__subclasses__()
        if len(grandchildren) > 0:
            l.extend(_get_class_hierarchy(t))
        else:
            l.append(t)
            
    return l
    
    
class EventFactory(object):
    """
    Factory for creating event objects corresponding to the different types of plays (events) in RTSS play by play data.
    Constructor selected based upon the event enum :py:class:`.EventType.Events` passed.
    """
    
    event_list = _get_class_hierarchy(Event)
    """List of available events loaded dynamically by following the subclass structure of :py:class:`.Event`."""
    
    @staticmethod
    def Create(event_type):
        """
        Factory method creates objects derived from :py:class`.Event` with class name matching the :py:class`.EventType`.
        
        :param event_type: number for type of event
        :returns: constructed event corresponding to ``event_type``
        :rtype: :py:class:`.Event`
        """
        if event_type in EventType.Name:
            # unknown event type gets base class
            if EventType.Name[event_type] == Event.__name__:
                return Event()
            else:
                # instantiate Event subclass with same name as EventType name
                return [t for t in EventFactory.event_list if t.__name__ == EventType.Name[event_type]][0]()
        else:
            raise TypeError("EventFactory.Create: Invalid EventType")
