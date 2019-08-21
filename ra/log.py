'''
A logging client.

Writes log messages on a local file, sys.stdout and to a udp log server.
The logger behaviour is changed with a LoggerAdapter to add an attribute
(`hostname`) to the formatter.
'''

import logging
import logging.handlers
import os
import pathlib
import socket
import sys


log = None


def setup_logger(filename='ra.log', srv_host=None, srv_port=None):

    global log

    logger = logging.getLogger('ra')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s:%(levelname)s:%(hostname)s'
        ':%(filename)s:%(funcName)s():%(lineno)d]'
        ': %(message)s'
    )

    fh = logging.FileHandler(filename=filename, mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # ch = logging.StreamHandler(stream=sys.stdout)
    # ch.setLevel(logging.DEBUG)
    # ch.setFormatter(formatter)
    # logger.addHandler(ch)

    if None not in (srv_host, srv_port):
        dh = logging.handlers.DatagramHandler(srv_host, srv_port)
        dh.setLevel(logging.DEBUG)
        dh.setFormatter(formatter)
        logger.addHandler(dh)

    adapter = logging.LoggerAdapter(logger, {'hostname': socket.gethostname()})
    log = adapter
    return log


def get_logger():
    if log is None:
        msg = 'Error: Logger not initialized, run setup_logger() beforehand'
        raise Exception(msg)
    return log


cwd = pathlib.Path(os.getcwd())
log = setup_logger(filename=str(cwd / 'ra.log'))
