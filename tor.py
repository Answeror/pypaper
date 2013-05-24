#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess as sp
from conf import conf


BASE_SOCKS_PORT = 9050
BASE_CONTROL_PORT = 8118
ROOT = os.path.dirname(__file__)
TOR_PATH = os.path.join(ROOT, 'tor', 'tor.exe')


class Tor(object):

    def __init__(self, channel_count):
        assert channel_count < 1024
        self.channel_count = channel_count
        _prepare_dir(channel_count)

    def run(self):
        for i in range(self.channel_count):
            socks_port = BASE_SOCKS_PORT + i
            control_port = BASE_CONTROL_PORT + i
            f = open(os.path.join(conf.tor_data_path, '%d.out' % i), 'wb')
            sp.Popen([
                TOR_PATH,
                '--RunAsDaemon',
                '1',
                '--CookieAuthentication',
                '0',
                '--HashedControlPassword',
                '',
                '--ControlPort',
                str(control_port),
                '--PidFile',
                os.path.join(conf.tor_data_path, '%d.pid' % i),
                '--SocksPort',
                str(socks_port),
                '--DataDirectory',
                _tor_data_path(i)
            ], stdout=f, stderr=f)


def _tor_data_path(i):
    return os.path.join(conf.tor_data_path, str(i))


def _prepare_dir(channel_count):
    _prepare_root_dir()
    for i in range(channel_count):
        _try_makedirs(_tor_data_path(i))


def _prepare_root_dir():
    _try_makedirs(conf.tor_data_path)


def _try_makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == '__main__':
    tor = Tor(2)
    tor.run()
    raw_input('press')
