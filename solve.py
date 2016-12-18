import configparser
import game
import logging
import os
from srhpytools_srh.options.parsers import ConfigFileParser
from srhpytools_srh.util import mylogging

logger = logging.getLogger('tri_peaks_solver.solve')

if __name__ == '__main__':
    # get command line options
    usage = '%(prog)s configfile [options]'
    parser = ConfigFileParser(usage=usage)
    opts = parser.parse_args()

    # set up logging
    mylogging.config_root_file_logger(logfn=opts.logfile, loglevel=opts.loglevel, logmode=opts.logmode)
    logger.setLevel(opts.loglevel)

    # get config file options
    cp = configparser.ConfigParser()
    cp.read(opts.configfile)

    # Can't believe configparser still does this
    try:
        game_fn = cp.get('Main', 'GameFile')
    except configparser.NoSectionError:
        if not os.path.isfile(opts.configfile):
            raise FileNotFoundError('no config file {}'.format(opts.configfile))
        else:
            raise

    # showtime
    g = game.game_from_file(game_fn)
    # TODO: add goal
    g.solve()
    # TODO: add logging
    # TODO: add unit tests
    input('any key')
