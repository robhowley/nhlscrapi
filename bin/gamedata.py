#!/usr/bin/env python

if __name__ == '__main__':
  import sys
  sys.path.append('../nhlscrapi')
  
  import json
  
  from cli_opts import cli_opts
  from nhlscrapi._tools import JSONDataEncoder as Encoder
  from nhlscrapi import constants as C
  from nhlscrapi.games.cumstats import ShotCt, ShotAttemptCt, Corsi, Fenwick
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
    'Shots': ShotCt(),
    'ShotAtt': ShotAttemptCt(),
    'Corsi': Corsi(),
    'Fenwick': Fenwick()
  }
  game = Game(gk, cum_stats=cum_stats)
  
  out_f = ''.join(str(x) for x in gk.to_tuple()) + '.json'
  # with open(out_f, 'w') as f:
  #   game.load_plays()
  #   print 'Shots         :', game.cum_stats['Shots'].total
  #   print 'Shot Attempts :', game.cum_stats['ShotAtt'].total
  #   print 'EV Shot Atts  :', game.cum_stats['Corsi'].total
  #   print 'Corsi         :', game.cum_stats['Corsi'].share()
  #   print 'FW Shot Atts  :', game.cum_stats['Fenwick'].total
  #   print 'Fenwick       :', game.cum_stats['Fenwick'].share()
    
    #f.write(json.dumps(game, cls=Encoder) + '\n')
  
  
#  for team, pls in game.load_rosters().iteritems():
#    print '\n%s Team' % team
#    for num, pl in pls.iteritems():
#      print num, pl
  
  # print '\nby property'
  # print 'Home'
  # for num, pl in game.home_roster.iteritems():
  #   print num, pl
    
  # print 'Away'
  # for num, pl in game.home_roster.iteritems():
  #   print num, pl
    
  # print game.match_up
  
  for team, coach in game.load_coaches().iteritems():
    print team, coach
    
  for ot, off in game.load_officials().iteritems():
    print ot, off