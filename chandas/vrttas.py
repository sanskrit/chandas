# -*- coding: utf-8 -*-
"""
    chandas.vrttas
    ~~~~~~~~~~~~~~

    Classes for representing various metrical forms.

    :license: MIT and BSD
"""

import re


class Vrtta(object):

    """Abstract base class for any metrical form"""


class Samavrtta(Vrtta):

    """A meter in which each line has the same syllable pattern."""

    def __init__(self, name, pattern):
        #: The name of the meter.
        self.name = name

        #: The scan for each pāda.
        self.pada_scan = [re.sub('[^LG]', '', x) for x in pattern] * 4
