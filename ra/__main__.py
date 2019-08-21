
import argparse
import os
import sys
import pathlib
from pprint import pprint
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
    run_simu.run(args['cfg_dir'])

main()
