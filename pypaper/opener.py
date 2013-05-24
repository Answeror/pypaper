#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .tor import Tor
from .socksipyhandler import SocksiPyHandler
from . import socks
import urllib2


class Opener(object):

    def __init__(self):
        self.tor = Tor()
        self.impl = urllib2.build_opener(SocksiPyHandler(
            socks.PROXY_TYPE_SOCKS4,
            'localhost',
            self.tor.socks_port
        ))

    def open(self, *args, **kargs):
        self.impl.open(*args, **kargs)
