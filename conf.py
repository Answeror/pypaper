#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class Conf(object):

    def __init__(self):
        self.tor_data_path = os.path.join('temp', 'tor')
        self.tor_base_socks_port = 9050
        self.tor_base_control_port = 8118


conf = Conf()
