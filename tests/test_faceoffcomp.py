import unittest

class TestFaceOffComparison(unittest.TestCase):

    def test_face_off_comparison(self):
        from nhlscrapi.games.game import GameKey
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
        
        # face off win %
        rnd = { k: round(v, 2) for k, v in foc.fo_pct.items() }
        self.assertEqual(rnd, { 'home': 0.57, 'away': 0.43 })
        
        # neut zone face off records
        self.assertEqual(foc.by_zone['away']['neut'], { 'won': 10, 'total': 24 })
        self.assertEqual(foc.by_zone['home']['neut'], { 'won': 14, 'total': 24 })
        
        # neut zone face off %
        self.assertEqual(round(foc.fo_pct_by_zone['away']['neut'],2), 0.42)
        
        # away off/home def zone face off records
        self.assertEqual(foc.by_zone['away']['off'], { 'won': 9, 'total': 23 })
        self.assertEqual(foc.by_zone['home']['def'], { 'won': 14, 'total': 23 })


if __name__ == '__main__':
    unittest.main()