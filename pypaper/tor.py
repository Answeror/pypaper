#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess as sp
import logging
from conf import conf


ROOT = os.path.dirname(__file__)
TOR_PATH = os.path.join(ROOT, 'tor', 'tor.exe')


class Tor(object):

    def __init__(
        self,
        root=conf.tor_data_path,
        socks_port=conf.tor_base_socks_port,
        control_port=conf.tor_base_control_port
    ):
        self._root = root
        self.socks_port = socks_port
        self.control_port = control_port

    @property
    def root(self):
        _try_makedirs(self._root)
        return self._root

    @property
    def datapath(self):
        d = os.path.join(self.root, 'data')
        _try_makedirs(d)
        return d

    @property
    def outpath(self):
        return os.path.join(self.root, 'out')

    @property
    def pidpath(self):
        return os.path.join(self.root, 'tor.pid')

    def run(self):
        try:
            self.f = open(self.outpath, 'wb')
            self.p = sp.Popen([
                TOR_PATH,
                '--RunAsDaemon',
                '1',
                '--CookieAuthentication',
                '0',
                '--HashedControlPassword',
                '',
                '--ControlPort',
                str(self.control_port),
                '--PidFile',
                self.pidpath,
                '--SocksPort',
                str(self.socks_port),
                '--DataDirectory',
                self.datapath
            ], stdout=self.f, stderr=self.f)
        except Exception as e:
            logging.exception(e)
            self.stop()
            raise

    def stop(self):
        if _notnone(self, 'f'):
            self.f.close()
            self.f = None
        if _notnone(self, 'p'):
            self.p.kill()
            self.p = None


def _notnone(self, name):
    return hasattr(self, name) and not getattr(self, name) is None


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
    tor = Tor()
    tor.run()
    raw_input('press')
    tor.stop()
