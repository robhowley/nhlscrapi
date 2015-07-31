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