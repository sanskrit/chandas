# -*- coding: utf-8 -*-
"""
    chandas.classify
    ~~~~~~~~~~~~~~~~

    Top-level code for identifying the meter of some raw input.

    :license: MIT
"""

import json

from .padyas import Ardhasamavrtta, Samavrtta, Vishamavrtta
from .wrappers import Verse

class Classifier(object):

    """Scans some raw input and identifies its meter."""

    def __init__(self, padyas):
        self.padyas = padyas

    @classmethod
    def from_json_file(self, path):
        """Create a Classifier from some JSON file.

        :param path: path to some JSON file.
        """
        with open(path) as f:
            data = json.load(f)

            class_map = {
                'samavrtta': Samavrtta,
                'ardhasamavrtta': Ardhasamavrtta,
                'vishamavrtta': Vishamavrtta,
            }
            padyas = []
            for category, examples in data.iteritems():
                cls = class_map[category]
                for vrtta in examples:
                    padyas.append(cls(vrtta['name'], vrtta['pattern']))
            return Classifier(padyas)

    def classify(self, raw):
        """Identify the meter of some input.

        :param raw: an input string
        """
        verse = Verse(raw)
        verse_scan = ''.join(verse.scan)
        for vrtta in self.padyas:
            if vrtta.regex.match(verse_scan):
                return vrtta
        return None
