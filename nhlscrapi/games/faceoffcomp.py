
from nhlscrapi.scrapr.faceoffrep import FaceOffRep
from nhlscrapi.games.repscrwrap import RepScrWrap, dispatch_loader


class FaceOffComparison(RepScrWrap):
    """
    Face-off Comparison and summary report. Produces the by player and head-to-head matchup face off totals
    by zone and overall. For either home or away the full summary data takes the following form
        {
            'home/away': {
                player_num: {
                    'off/def/neut/all': { 'won': won, 'total': total }
                }
            }
        }
    """
    
    def __init__(self, game_key):
        super(FaceOffComparison, self).__init__(game_key, FaceOffRep(game_key))
        self.__team_tots = None
        self.__zones = [ 'off', 'def', 'neut', 'all' ]
        
    @property
    @dispatch_loader('_rep_reader', 'parse_home_face_offs')
    def home_fo(self):
        """
        Property that returns the full by player face-off summary for the home team. See FaceOffComparison
        for dictionary key structure.
        
        :returns: dict
        """
        return self._rep_reader.face_offs['home']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_away_face_offs')
    def away_fo(self):
        """
        Property that returns the full by player face-off summary for the away team. See FaceOffComparison
        for dictionary key structure.
        
        :returns: dict
        """
        return self._rep_reader.face_offs['away']
    
    def head_to_head(self, home_num, away_num):
        """
        Return the head-to-head face-off outcomes between two players.
        If the matchup happened, then the format of the output is
            {
                'home': { 'off/def/neut/all': { 'won': won, 'total': total } }
                'away': { 'off/def/neut/all': { 'won': won, 'total': total } }
            }
        else an empty { } dictionary will be returned
        
        :param home_num: the number of the home team player
        :param away_num: the number of the away team player
        :returns: dict described above or { }
        """
        h_fo = self.home_fo[home_num]['opps'][away_num]
        a_fo = self.away_fo[away_num]['opps'][home_num]
        return {
            'home': { k: h_fo[k] for k in self.__zones },
            'away': { k: a_fo[k] for k in self.__zones }
        }

    @property
    def team_totals(self):
        """
        Returns the overall faceoff win/total breakdown for home and away as
            {
                'home/away': { 'won': won, 'total': total }
            }
        
        :returns: dict
        """
        if self.__team_tots is None:
            self.__team_tots = self.__comp_tot()
        
        return {
            t: self.__team_tots[t]['all']
            for t in [ 'home', 'away' ]
        }

    @property
    def by_zone(self):
        """
        Returns the faceoff win/total breakdown by zone for home and away as
            {
                'home/away': {
                    'off/def/neut': { 'won': won, 'total': total }
                }
            }
        
        :returns: dict
        """
        if self.__team_tots is None:
            self.__team_tots = self.__comp_tot()
        
        return {
            t: {
                z: self.__team_tots[t][z]
                for z in self.__zones
                if z != 'all'
            }
            for t in [ 'home', 'away' ]
        }
       
    @property
    def fo_pct(self):
        """
        Get the by team overall face-off win %. Format is { 'home': %, 'away': % }
        
        :returns: dict
        """
        tots = self.team_totals
        return {
            t: tots[t]['won']/(1.0*tots[t]['total']) if tots[t]['total'] else 0.0
            for t in [ 'home', 'away' ]
        }
        
    @property
    def fo_pct_by_zone(self):
        """
        Get the by team face-off win % by zone. Format is
            {
                'home/away': { 'off/def/neut': % }
            }
            
        :returns: dict
        """
        bz = self.by_zone
        return {
            t: {
                z: bz[t][z]['won']/(1.0*bz[t][z]['total']) if bz[t][z]['total'] else 0.0
                for z in self.__zones
                if z != 'all'
            }
            for t in [ 'home', 'away' ]
            
        }
        
    def __comp_tot(self):
        def tbz(fos):
            r = {
                z: { 'won': 0, 'total': 0 }
                for z in self.__zones
            }
            
            for _, d in fos.items():
                for z in self.__zones:
                    r[z]['won'] += d[z]['won']
                    r[z]['total'] += d[z]['total']
            return r
            
        return {
            'home': tbz(self.home_fo),
            'away': tbz(self.away_fo)
        }