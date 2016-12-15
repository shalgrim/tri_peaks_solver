import game
from srhpytools_srh.options.parsers import ConfigFileParser

if __name__ == '__main__':
    # TODO: add config file parser
    cfp = ConfigFileParser('Usage: python solve.py config_file [options]')
    logfile = cfp.logfile
    loglevel = cfp.logleve
    g = game.game_from_file(fn)
    # TODO: add goal
    g.solve()
    # TODO: add logging
    # TODO: add unit tests
    input('any key')