#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import subprocess as sp
import logging
import shutil
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

    def run(self, block=False):
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
            if not block:
                return self.running
            else:
                for i in range(10):
                    if self.running:
                        return True
                    time.sleep(3)
                return False
        except Exception as e:
            logging.exception(e)
            self.stop()
            raise

    @property
    def running(self):
        if not os.path.exists(output_path(self.root)):
            return False
        return read_output(self.root)[-2:] == [
            'Opening Socks listener on 127.0.0.1:%d' % self.socks_port,
            'Opening Control listener on 127.0.0.1:%d' % self.control_port
        ]

    def stop(self):
        if _notnone(self, 'p'):
            self.p.kill()
            win_kill(self.p.pid)
            del self.p
            self.p = None
        if _notnone(self, 'f'):
            self.f.close()
            self.f = None
        try:
            os.remove(output_path(self.root))
        except:
            pass


def win_kill(pid):
    '''kill a process by specified PID in windows'''
    import win32api
    import win32con

    hProc = None
    try:
        hProc = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid)
        win32api.TerminateProcess(hProc, 0)
    except Exception:
        return False
    finally:
        if hProc is not None:
            hProc.Close()

    return True


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


def output_path(root):
    return os.path.join(root, 'out')


def read_output(root):
    try:
        with open(output_path(root), 'r') as f:
            return [trim(line.decode('utf-8')) for line in f]
    except:
        return []


def trim(s):
    import re
    ret = re.search(r'.*\[\w+\] (.*)', s)
    assert ret
    return ret.group(1).strip()


if __name__ == '__main__':
    tor = Tor()
    tor.run()
    raw_input('press')
    tor.stop()
