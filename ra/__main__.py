
import argparse
import os
import sys
import pathlib
import signal

from ra import run_simu
from ra.log import log


def sigint_handler(sig, frame):
    log.debug('Interrupted by user with Ctrl+C!')
    sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='ra',
        description='Room Acoustics.'
    )
    parser.add_argument(
        '-c', '--cfg-dir',
        help='Path pointing to dir with simulation configuration files.',
        required=True
    )
    args = vars(parser.parse_args())
    log.debug('Parsed arguments: {}'.format(args))
    return args


def main():
    args = parse_args()
    signal.signal(signal.SIGINT, sigint_handler)
    cfgs = run_simu.setup(args['cfg_dir'])
    run_simu.run(cfgs)


if __name__ == '__main__':
    main()
