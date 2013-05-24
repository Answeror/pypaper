#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class Conf(object):

    def __init__(self):
        self.tor_data_path = os.path.join('temp', 'tor')


conf = Conf()
