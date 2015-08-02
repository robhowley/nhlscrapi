import unittest

class TestTOIShiftSummary(unittest.TestCase):

    def test_toi_shift_summary(self):
        from nhlscrapi.games.game import GameKey
        from nhlscrapi.games.toi import TOI
       
        toi = TOI(game_key=GameKey(2015,3,224))  # 2015, playoffs (3), NYR/WSH game 3 (game 224)

        try:
            toi.load_all()
        except Exception as e:
            self.assertEqual(0, 1, 'Loading error: {0}'.format(e))
        
        def get_most(shift_d, ex):
            return sorted(
                ((pn, sh) for pn, sh in shift_d.items() if pn not in ex),
                key=lambda k: -(k[1].game_summ['toi']['min']*60+k[1].game_summ['toi']['sec'])
            )[0]
            
        # players with most TOI excluding goalies
        # for home team, exclude number 70: Holty
        most_home_num, most_home_summ = get_most(toi.home_shift_summ, [70])
        # for away, exclude number 30: Lundqvist
        most_away_num, most_away_summ = get_most(toi.away_shift_summ, [30])
            
        # niskanen played 23:19
        self.assertEqual(most_home_num, 2)
        self.assertEqual(most_home_summ.game_summ['toi'], { 'min': 23, 'sec': 19 })
        
        # mcdonagh played 23:52
        self.assertEqual(most_away_num, 27)
        self.assertEqual(most_away_summ.game_summ['toi'], { 'min': 23, 'sec': 52 })


if __name__ == '__main__':
    unittest.main()