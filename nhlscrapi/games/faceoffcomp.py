
from nhlscrapi.scrapr.faceoffrep import FaceOffRep
from nhlscrapi.games.repscrwrap import RepScrWrap, dispatch_loader


class FaceOffComparison(RepScrWrap):
    def __init__(self, game_key):
        super(FaceOffComparison, self).__init__(game_key, FaceOffRep(game_key))
        
    @property
    @dispatch_loader('_rep_reader', 'parse_home_face_offs')
    def home_fo(self):
        return self._rep_reader.face_offs['home']
        
    @property
    @dispatch_loader('_rep_reader', 'parse_away_face_offs')
    def away_fo(self):
        return self._rep_reader.face_offs['away']
    
    @dispatch_loader('_rep_reader', 'parse_away_face_offs')
    @dispatch_loader('_rep_reader', 'parse_home_face_offs')
    def head_to_head(self, home_num, away_num):
        h_fo = self._rep_reader.face_offs['home'][home_num]['opps'][away_num]
        a_fo = self._rep_reader.face_offs['away'][away_num]['opps'][home_num]
        zones = [ 'off', 'def', 'neut', 'all' ]
        return {
            'home': { k: h_fo[k] for k in zones },
            'away': { k: a_fo[k] for k in zones }
        }
