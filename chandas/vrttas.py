# -*- coding: utf-8 -*-
"""
    chandas.vrttas
    ~~~~~~~~~~~~~~

    TODO: write description

    :license: MIT and BSD
"""

import re


class Vrtta(object):
    pass


class Samavrtta(Vrtta):
    def __init__(self, name, pattern):
        #: The name of the meter.
        self.name = name

        #: The scan for each pāda.
        self.pada_scan = [re.sub('[^LG]', '', x) for x in pattern] * 4
