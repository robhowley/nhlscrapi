
# for the play parser
import nhlscrapi.constants as c
from nhlscrapi._tools import to_int
from nhlscrapi.scrapr.eventparser import event_type_mapper, parse_event_desc

# base for RTSS
from nhlscrapi.scrapr.reportloader import ReportLoader


class RTSS(ReportLoader):
    """Retrieve and load RTSS play by play game data"""
  
    def __init__(self, game_key):
        super(RTSS, self).__init__(game_key, "rtss")
        
        self.plays = []
        """List of plays loaded. See :py:class:`.PlayParser` for play data structure."""
        
        
    def parse(self):
        """
        Parse full document. Plays and matchups.
        
        :returns: ``self`` on success, ``None`` otherwise
        """

        try:
            return super(RTSS, self).parse().parse_plays()
        except:
            return None
        
        
    def parse_plays(self):
        """
        Retreive and parse Play by Play data for the given :py:class:`nhlscrapi.games.GameKey`
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        
        try:
            self.plays = [p for p in self.parse_plays_stream()]
            return self
        except:
            return None
        
        
    def parse_plays_stream(self):
        """Generate and yield a stream of parsed plays. Useful for per play processing."""
        
        lx_doc = self.html_doc()
        if lx_doc is not None:
            parser = PlayParser(self.game_key.season, self.game_key.game_type)
            plays = lx_doc.xpath('//tr[@class = "evenColor"]')
            for p in plays:
                p_obj = parser.build_play(p)
                self.plays.append(p_obj)
                
                yield p_obj
                
                
# will take a RTSS play table row and return a Play object
class PlayParser(object):
    """Interprets a single RTSS play by play table row, i.e. a single play. Constructs a dictionary of play features."""
    
    def __init__(self, season = c.MAX_SEASON, game_type=None):
        self.season = season
        self.game_type = game_type
    
    @staticmethod
    def ColMap(season):
        """
        Returns a dictionary mapping the type of information in the RTSS play row to the
        appropriate column number. The column locations pre/post 2008 are different.
        
        :param season: int for the season number
        :returns: mapping of RTSS column to info type
        :rtype: dict, keys are ``'play_num', 'per', 'str', 'time', 'event', 'desc', 'vis', 'home'``
        """
        if c.MIN_SEASON <= season <= c.MAX_SEASON:
            return {
                "play_num": 0,
                "per": 1,
                "str": 2,
                "time": 3,
                "event": 4,
                "desc": 5,
                "vis": 6,
                "home": 7
            }
        else:
            raise ValueError("RTSSCol.MAP(season): Invalid season " + str(season))
    
    def build_play(self, pbp_row):
        """
        Parses table row from RTSS. These are the rows tagged with ``<tr class='evenColor' ... >``. Result set
        contains :py:class:`nhlscrapi.games.playbyplay.Strength` and :py:class:`nhlscrapi.games.events.EventType`
        objects. Returned play data is in the form
        
        .. code:: python
        
            {
                'play_num': num_of_play
                'period': curr_period
                'strength': strength_enum
                'time': { 'min': min, 'sec': sec }
                'vis_on_ice': { 'player_num': player }
                'home_on_ice': { 'player_num': player }
                'event': event_object
            }
        
        :param pbp_row: table row from RTSS
        :returns: play data
        :rtype: dict
        """
        d = pbp_row.findall('./td')
        c = PlayParser.ColMap(self.season)
        
        p = { }
        to_dig = lambda t: int(t) if t.isdigit() else 0
        p['play_num'] = to_int(d[c["play_num"]].text, 0)
        p['period'] = to_int(d[c["per"]].text, 0)
        
        p['strength'] = self.__strength(d[c["str"]].text)
        
        time = d[c["time"]].text.split(":")
        p['time'] = { "min": int(time[0]), "sec": int(time[1]) }
        
        skater_tab = d[c["vis"]].xpath("./table")
        p['vis_on_ice'] = self.__skaters(skater_tab[0][0]) if len(skater_tab) else { }
            
        skater_tab = d[c["home"]].xpath("./table")
        p['home_on_ice'] = self.__skaters(skater_tab[0][0]) if len(skater_tab) else { }
            
        p['event'] = event_type_mapper(
            d[c["event"]].text,
            period=p['period'],
            skater_ct=len(p['vis_on_ice']) + len(p['home_on_ice']),
            game_type=self.game_type
        )
        p['event'].desc = " ".join([str(t.encode('ascii', 'replace')) for t in d[c["desc"]].xpath("text()")])
        parse_event_desc(p['event'], season=self.season)
        
        return p
        
    def __skaters(self, tab):
        """
        Constructs dictionary of players on the ice in the provided table at time of play.
        :param tab: RTSS table of the skaters and goalie on at the time of the play
        :rtype: dictionary, key = player number, value = [position, name]
        """
        
        res = { }
        for td in tab.iterchildren():
            if len(td):
                pl_data = td.xpath("./table/tr")
                pl = pl_data[0].xpath("./td/font")
                
                if pl[0].text.isdigit():
                    res[int(pl[0].text)] = [s.strip() for s in pl[0].get("title").split("-")][::-1]
                
                s = pl[0].get("title").split("-")
                pos = pl_data[1].getchildren()[0].text
                
        return res
        
    def __strength(self, sg_str):
        # avoids the circular import, but wreaks of code that needs refactoring
        from nhlscrapi.games.playbyplay import Strength
        
        if 'PP' in sg_str:
            return Strength.PP
        elif 'SH' in sg_str:
            return Strength.SH
        else:
            return Strength.Even
