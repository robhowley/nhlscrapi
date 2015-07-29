import unittest

# TODO: load a game, parse events, assert final score

class TestRTSSParse(unittest.TestCase):

    def test_face_off_comparison(self):
        from nhlscrapi.games.gamekey import GameKey
        from nhlscrapi.games.faceoffcomp import FaceOffComparison

        gk = GameKey(2015,3,224)        # 2015, playoffs (3), NYR/WSH game 3 (game 224)
        foc = FaceOffComparison(gk)

        try:
            foc.load_all()
            hth = foc.head_to_head(21, 21)  # laich v stepan
        except Exception as e:
            self.assertEqual(0, 1, 'Loading error: {0}'.format(e))
            
        # stepan 2/4 overall
        self.assertEqual(hth['away']['all'], { 'won': 2, 'total': 4 })
            
        # laich 1/1 in the defensive zone
        self.assertEqual(hth['home']['def'], { 'won': 1, 'total': 1 })
            
        # equivalently, stepan 0/1 in offensive
        self.assertEqual(hth['away']['off'], { 'won': 0, 'total': 1 })

        