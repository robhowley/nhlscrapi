v0.3.7
------

  * messed up the prior upload. embarrassing. fixed remaining 3.x print issue.

v0.3.6
------

  * fixed a lot of python3.x compatibility issues

    - ``_tools.build_enum`` switch to ``items()`` from ``iteritems()``
    - ``print vs`` to ``print()`` in ``scrapr.descparser``
    - take out ``maketrans`` in ``scrapr.descparser`` and put in ``replace()``

  * fully qualify the ``scrapr.eventparser`` import in ``scrapr.rtss``
  * ``Game.plays`` property returns ``self.play_by_play.plays()`` but plays isn't callable

v0.3.5
------

  * dropped urllib2 dependency because it's 2015 and I'm tired of being a dinosaur
  * added ``requests`` to setup dependencies
  * fully qualified the ``scrapr.NHLCn`` import in ``scrapr.reportloader``
  * consolidated cli_opts.py into gamedata.py ... that whole thing needs a rewrite anyway (TODO)

v0.3.4
------

  * setup script reference bug.

v0.3.3
------

  * true bug fix. messed up the pypi upload setup
  * forgot cfg et c.

v0.3.2
------

  * refactored ``Plays``/``Strength`` construct

    - moved ``Plays`` and ``Strength`` from ``games.plays`` to ``games.playbyplay``
    - moved ``scrapr.rtss.playparser.PlayParser`` to ``scrapr.rtss``
    - deleted games/plays.py and scrapr/playparser.py
    - reworked data structure of ``PlayParser`` to be purely a dict
    - parsed play data isn't converted into the proper ``Play`` object until ``games.playbyplay.PlayByPlay`` gets it

  * refactored TOI/ShiftSummary construct

    - moved ``ShiftSummary`` from ``scrapr.toirep`` to ``games.toi``
    - ``scrapr.toirep.TOIRepBase`` now stores by player shift info as dict
    - parsed shift summary isn't made into a ``ShiftSummary`` object until in ``TOI``

  * Goal of both big refactors was to keep scraping/raw web data as dicts and have object wrappers only exist in the games package
  * added a ``unittest`` for the time on ice and shift summary info
  * added docstrings to major report and scraper interfaces
  * built docs using Sphinx


v0.3.1
------

  * fixed play-by-play bug created when no cum_stats provided
  * deprecated extractors
  * refactored GameKey and GameType into nhlscrapi.games.game
  * updated unittests and README to reflect the refactoring


v0.3.0
------

  * added face off comparison report, associated report loaded (scraper) and unittest

    * gave Game object basic access/loading to face off comp

  * reworked testing framework

    * can now run tests w the standard :code:`python -m unittest discover`

  * made versioning counter sane. structure is v(realease).(feature).(bug)
  * added :code:`lxml` to the install requirements in setup
  * added this change log