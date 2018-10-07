"""Entrypoint for CLI"""

import logging
import argparse

from bci_learning_studio import __version__

VERSION_STRING = 'BCI Learning Studio {}'.format(__version__)


def _parse_args():
    parser = argparse.ArgumentParser(
        description='Start BCI learning studio.',
    )
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--version', action='version', version=VERSION_STRING)
    namespace, args = parser.parse_known_args()

    if namespace.debug:
        # it's often useful to be able to access debug flag in sub command
        args.append('--debug')
    return namespace, args


def main():
    """Entrypoint for `openbci_interface` command"""
    namespace, args = _parse_args()
    _init_logger(namespace.debug)
    raise NotImplementedError('Not implemented yet...')


def _init_logger(debug=False):
    """Initialize logger"""
    header = '%(asctime)s: %(levelname)5s'
    if debug:
        header += ' %(funcName)10s %(lineno)d'
    format_ = '{}: %(message)s'.format(header)
    logging.basicConfig(
        format=format_,
        level=logging.DEBUG if debug else logging.INFO,
    )


if __name__ == '__main__':
    main()
