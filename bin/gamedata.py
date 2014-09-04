#!/usr/bin/env python

if __name__ == '__main__':
  import sys
  sys.path.append('../nhlscrapi')
  
  import json
  
  from cli_opts import cli_opts
  from nhlscrapi._tools import JSONDataEncoder as Encoder
  from nhlscrapi import constants as C
  from nhlscrapi.games.cumstats import Score, ShotCt, ShotAttemptCt, Corsi, Fenwick
  from nhlscrapi.games.game import Game
  from nhlscrapi.games.gamekey import GameKey, GameType
  
  # get cli opts
  def get_inp_params(args):
    # define input parameters and validators
    inp = {
      '-s': [lambda s: s.isdigit() and int(s) in C.GAME_CT_DICT, lambda s: int(s)],
      '-g': [lambda g: g.isdigit(), lambda g: int(g)],
      '-r': [lambda r: r.isdigit() and int(r) in [0,1], lambda r: int(r) > 0]
    }
    
    call_conv = "gamedata.py -s <season, integer> -g <game_num, integer> -r <reg_season, binary>"
    
    out = cli_opts(args, inp, call_conv)
    return out['-s'], out['-g'], out['-r']
  
  # start script
  season, game_num, reg_season = get_inp_params(sys.argv[1:])
  
  if not 1 <= game_num <= C.GAME_CT_DICT[season]:
    print 'Invalide game number: %i' % game_num
    sys.exit(0)
    
  print season, game_num, reg_season
  
  gt = GameType.Regular if reg_season else GameType.Playoffs
  gk = GameKey(season, gt, game_num)
  cum_stats = {
    'Score': Score(),
    'Shots': ShotCt(),
    'ShotAtt': ShotAttemptCt(),
    'Corsi': Corsi(),
    'Fenwick': Fenwick()
  }
  game = Game(gk, cum_stats=cum_stats)
  
  out_f = ''.join(str(x) for x in gk.to_tuple()) + '.json'
#  with open(out_f, 'w') as f:
    # game.load_plays()
    # game.load_all_personnel()
    
    # print 'Final         :', game.cum_stats['Score'].total
    # print 'Shootout      :', game.cum_stats['Score'].shootout.total
    # print 'Shots         :', game.cum_stats['Shots'].total
    # print 'Shot Attempts :', game.cum_stats['ShotAtt'].total
    # print 'EV Shot Atts  :', game.cum_stats['Corsi'].total
    # print 'Corsi         :', game.cum_stats['Corsi'].share()
    # print 'FW Shot Atts  :', game.cum_stats['Fenwick'].total
    # print 'Fenwick       :', game.cum_stats['Fenwick'].share()
    
    #f.write(json.dumps(game, cls=Encoder) + '\n')
    
  #from nhlscrapi.scrapr.toi import TOIRepBase
  #toi = TOIRepBase(gk, 'away_toi')
  #print toi.parse_matchup()
  #print toi.parse_shifts()
  #print game.load_home_toi()
  #print game.matchup
  print game.rosters.away_scratches()
  print 'do it again ... better not load'
  print game.rosters.away_scratches()
  
  print '\nPlay by plays first load'
  game.play_by_play.plays()
  
  print '\nPlay by plays second load'
  game.play_by_play.compute_stats()
  print game.play_by_play.cum_stats['Score'].total