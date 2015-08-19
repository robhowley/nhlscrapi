import unittest

class TestEventSummary(unittest.TestCase):

    def test_event_summary(self):
        from nhlscrapi.games.game import GameKey
        from nhlscrapi.games.eventsummary import EventSummary

        gk = GameKey(2015,3,224)        # 2015, playoffs (3), NYR/WSH game 3 (game 224)
        es = EventSummary(gk)

        try:
            es.load_all()
        except Exception as e:
            self.assertEqual(0, 1, 'Loading error: {0}'.format(e))
            
        # brassard: 1G, 0A, 1P, and AVG 35 secs per shift
        pl = es.away_players[16]
        self.assertEqual((pl['g'], pl['a'], pl['p']), (1, 0, 1))
        self.assertEqual(pl['toi']['avg'], { 'min': 0, 'sec': 35 })
            
        # washington team totals
        self.assertEqual(es.totals()['home'], {
            'g': 2,
            'a': 2,
            'p': 4,
            'pm': 5,
            'pn': 6,
            'pim': 23,
            's': 30,
            'ab': 7,
            'ms': 12,
            'ht': 37,
            'gv': 14,
            'tk': 7,
            'bs': 25,
            'fo': { 'won': 38, 'total': 67 }
        })
        
        # 2 niskanen had the highest toi for wash
        # 27 mcdonagh had the highest toi for ny
        top_toi = es.top_toi()
        self.assertEqual(top_toi['home']['num'], 2)
        self.assertEqual(top_toi['away']['num'], 27)
        
        # 6 diff players had penalties for washing
        # 4 diff playershad penalties for ny
        pens = es.had_penalties()
        self.assertEqual(len(pens['home']), 6)
        self.assertEqual(len(pens['away']), 4)
        
        # 1 goal scorer for wash
        self.assertEqual(len(es.goal_scorers()['home']), 1)
        
        # 3 point getters for ny
        self.assertEqual(len(es.point_getters()['away']), 3)
        
        # 3 wilson had most pims on wash
        self.assertEqual(es.top_by_key(sort_key='pim')['home']['num'], 43)


if __name__ == '__main__':
    unittest.main()