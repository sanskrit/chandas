# -*- coding: utf-8 -*-
"""
    chandas.vrttas
    ~~~~~~~~~~~~~~

    Classes for representing various metrical forms.

    :license: MIT and BSD
"""

import re


class Vrtta(object):

    """Abstract base class for a metrical form."""

    def __init__(self, name, pattern):
        #: The name of the meter.
        self.name = name

        #: The scan for each pāda.
        self.scans = [self._clean(pada) for pada in pattern]

    @classmethod
    def _clean(self, data):
        return re.sub('[^LG]', '', data)

    def __repr__(self):
        return "<{}('{}')>".format(self.__class__.__name__, self.name)

    @property
    def regex(self):
        """Return a regex to test if some input matches the vrtta."""
        odd = self.scans[0]
        even = self.scans[0][:-1] + '[LG]'
        return re.compile(odd + even + odd + even)


class Samavrtta(Vrtta):

    """Represents a type of sama-vṛtta."""

    def __init__(self, name, pattern):
        assert len(pattern) == 1
        Vrtta.__init__(self, name, pattern * 4)


class Ardhasamavrtta(Vrtta):

    """Represents a type of ardha-sama-vṛtta."""

    def __init__(self, name, pattern):
        assert len(pattern) == 2
        Vrtta.__init__(self, name, pattern * 2)


class Vishamavrtta(Vrtta):

    """Represents a type of viṣama-vṛtta."""

    def __init__(self, name, pattern):
        assert len(pattern) == 4
        Vrtta.__init__(self, name, pattern)
