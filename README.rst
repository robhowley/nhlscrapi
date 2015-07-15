nhlscrapi: NHL Scrapr API
===============================

Purpose
--------

Provide a Python API for accessing NHL game data including play by play, game summaries, player stats et c. The library hides the guts of the NHL website scraping process and encapsulates not only the data gathering, but data output. This project is inspired by the `R <http://www.r-project.org>`_ package *nhlscrapr*, an all around must for NHL analytics geeks and R power users.

nhlscrapi is in the early/initial stages, but will be updated regularly.

Related projects:
  - `nhlscrapr <http://cran.r-project.org/web/packages/nhlscrapr/index.html>`_
  - `py-nhl <https://github.com/wellsoliver/py-nhl>`_

Usage Example
--------------
Scrape data for game 1226 of 2014, Ottawa vs Pittsburgh.

.. code-block:: python

  from nhlscrapi.games.game import Game
  from nhlscrapi.games.gamekey import GameKey, GameType
  from nhlscrapi.games.cumstats import Score, ShotCt, Corsi, Fenwick

  season = 2014                                    # 2013-2014 season
  game_num = 1230                                  # last game of the season
  game_type = GameType.Regular                     # regular season game
  game_key = GameKey(season, game_type, game_num)

  # define stat types that will be counted as the plays are parsed
  cum_stats = {
    'Score': Score(),
    'Shots': ShotCt(),
    'Corsi': Corsi(),
    'Fenwick': Fenwick()
  }
  game = Game(game_key, cum_stats=cum_stats)

  # also http requests and processing are lazy
  # accumulators require play by play info so they parse the RTSS PBP
  print 'Final         :', game.cum_stats['Score'].total
  print 'Shootout      :', game.cum_stats['Score'].shootout.total
  print 'Shots         :', game.cum_stats['Shots'].total
  print 'EV Shot Atts  :', game.cum_stats['Corsi'].total
  print 'Corsi         :', game.cum_stats['Corsi'].share()
  print 'FW Shot Atts  :', game.cum_stats['Fenwick'].total
  print 'Fenwick       :', game.cum_stats['Fenwick'].share()

  # http req for roster report
  # only parses the sections related to officials and coaches
  print '\nRefs          :', game.refs
  print 'Linesman      :', game.linesman
  print 'Coaches'
  print '  Home        :', game.home_coach
  print '  Away        :', game.away_coach

  # scrape all remaining reports
  game.load_all()

Current Release: v0.0.1
------------------------
This is a pre-release and is not stable and fully fit for production. The first full stable release (v0.1.0) will be made available once the framework for all `NHL RTSS reports <http://www.nhl.com/ice/gamestats.htm?fetchKey=20142ALLSATAll&sort=gameDate&viewName=teamRTSSreports>`_ is completed. Currently, Play-by-Play, Home/Away TOI and Roster reports are functional.


License
--------
The NHL Scrapr API is a free Python library provided under Apache License version 2.0.

  - Free software: Apache License, v2.0
  - Documentation: (coming eventually)
