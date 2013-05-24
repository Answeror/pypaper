#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .tor import Tor
from .socksipyhandler import SocksiPyHandler
from . import socks
import urllib2
from urllib2 import HTTPError, URLError
import logging
import time


class Opener(object):

    def __init__(self, timeout=60):
        self.tor = Tor()
        self.impl = _make_impl(self.tor.socks_port)
        self.timeout = timeout

    def _change_tor(self):
        self.tor.stop()
        self._run_tor()

    def __del__(self):
        self.tor.stop()

    def _run_tor(self):
        if not self.tor.running:
            if not self.tor.run(block=True):
                raise Exception('setup tor failed')

    def open(self, *args, **kargs):
        start_time = time.time()
        self._run_tor()
        while True:
            try:
                assert self.tor.running
                return self.impl.open(*args, **kargs)
            except HTTPError as e:
                elapsed = time.time() - start_time
                if elapsed > self.timeout:
                    logging.info('use %f seconds, timeout' % elapsed)
                    raise
                logging.info('http %d, change tor' % e.code)
                self._change_tor()
            except URLError as e:
                logging.info('url error, change tor')
                self._change_tor()
        assert False


def _make_impl(socks_port):
    return urllib2.build_opener(SocksiPyHandler(
        socks.PROXY_TYPE_SOCKS4,
        'localhost',
        socks_port
    ))
