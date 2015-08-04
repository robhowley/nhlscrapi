#!/usr/bin/env python

# parse command line options
def cli_opts(argv, inp, call_conv):
  import sys, getopt
  
  def print_ft_exit():
    print call_conv
    sys.exit(2)
    
  try:
    opts, args = getopt.getopt(argv, ':'.join(inp.keys()) + ':')
  except getopt.GetoptError as e:
    print_ft_exit()
    print e
  except Exception as e:
    print e
    
  if len(opts) != len(inp):
    print 'Invalid option count'
    print_ft_exit()
  
  out = { }
  for opt, arg in opts:
    if opt in inp.keys():
      if inp[opt][0](arg):
        out[opt] = inp[opt][1](arg)
      else:
        print 'Invalid input type for argument %s' % opt
        print_ft_exit()
    else:
      print 'No option of form %s' % opt
      print_ft_exit()
    
  return out
  

if __name__ == '__main__':
  
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
  with open(out_f, 'w') as f:
    
    # auto computes when using game wrapper
    # print 'Final         :', game.cum_stats['Score'].total
    # print 'Shootout      :', game.cum_stats['Score'].shootout.total
    # print 'Shots         :', game.cum_stats['Shots'].total
    # print 'Shot Attempts :', game.cum_stats['ShotAtt'].total
    # print 'EV Shot Atts  :', game.cum_stats['Corsi'].total
    # print 'Corsi         :', game.cum_stats['Corsi'].share()
    # print 'FW Shot Atts  :', game.cum_stats['Fenwick'].total
    # print 'Fenwick       :', game.cum_stats['Fenwick'].share()
    
    # print '\nRefs          :', game.refs
    # print 'Linesman      :', game.linesman
    # print 'Coaches'
    # print '  Home        :', game.home_coach
    # print '  Away        :', game.away_coach
    
    #f.write(json.dumps(game, cls=Encoder) + '\n')
    
    from nhlscrapi.scrapr.gamesummrep import GameSummRep
    summ = GameSummRep(gk)
    print(summ.parse_matchup())
    summ.parse_scoring_summary()