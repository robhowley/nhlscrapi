import unittest

# TODO: load a game, parse events, assert final score

class TestRTSSParse(unittest.TestCase):

    def test_game(self):
        from nhlscrapi.games.game import Game, GameKey, GameType
        from nhlscrapi.games.cumstats import Score, ShotCt, EvenStShotCt, Corsi, Fenwick
            
        fin_score = { }
        try:
            
            season = 2014                                    # 2013-2014 season
            game_num = 1226                                  #
            game_type = GameType.Regular                     # regular season game
            game_key = GameKey(season, game_type, game_num)
            
            # define stat types that will be counted as the plays are parsed
            cum_stats = {
              'Score': Score(),
              'Shots': ShotCt(),
              'EvenShots': EvenStShotCt(),
              'Corsi': Corsi(),
              'Fenwick': Fenwick()
            }
            game = Game(game_key, cum_stats=cum_stats)
            
            # will call all the http reqs (bc lazy)
            fin_score = game.cum_stats['Score']
        except Exception as e:
            self.assertEqual(0, 1, 'Loading error: {0}'.format(e))
        
        # final score test
        self.assertEqual(fin_score.total, { 'OTT': 3, 'PIT': 2 }, 'Incorrect final score: {}'.format(fin_score.total))
        
        # shootout goal tally test
        test_val = fin_score.shootout.total['OTT']
        self.assertEqual(test_val, 2, 'Incorrect OTT shootout goal count: {}'.format(test_val))
        
        # shot count test
        test_val = game.cum_stats['Shots'].total
        self.assertEqual(test_val, {'PIT': 28, 'OTT': 33}, 'Invalid shot count: {}'.format(test_val))
        
        # even strength shot count test
        test_val = game.cum_stats['EvenShots'].total
        self.assertEqual(test_val, {'PIT': 22, 'OTT': 18}, 'Invalid even strength shot count: {}'.format(test_val))
        
        # even strength shot attempt (corsi) test
        test_val = game.cum_stats['Corsi'].total
        self.assertEqual(test_val, {'PIT': 36, 'OTT': 39}, 'Invalid (Corsi) shot attempt count: {}'.format(test_val))
        
        # even strength, close, shot attempts ex blocks/misses (Fenwick) test
        test_val = game.cum_stats['Fenwick'].total
        self.assertEqual(test_val, {'PIT': 30, 'OTT': 29}, 'Invalid (Fenwick) shot attempt count: {}'.format(test_val))


if __name__ == '__main__':
    unittest.main()
