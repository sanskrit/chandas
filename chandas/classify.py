# -*- coding: utf-8 -*-
"""
    chandas.classify
    ~~~~~~~~~~~~~~~~

    Top-level code for identifying the meter of some raw input.

    :license: MIT
"""

import json

from .padyas import Ardhasamavrtta, Jati, Samavrtta, Vishamavrtta
from .wrappers import Verse


class Classifier(object):

    """Scans some raw input and identifies its meter."""

    def __init__(self, vrttas=None, jatis=None):
        self.vrttas = vrttas or []
        self.jatis = jatis or []

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
                'jati': Jati,
            }
            vrttas = []
            jatis = []
            for category, catalog in data.iteritems():
                padyas = (class_map[category](**item) for item in catalog)
                if category == 'jati':
                    jatis.extend(padyas)
                else:
                    vrttas.extend(padyas)
            return Classifier(vrttas=vrttas, jatis=jatis)

    def classify(self, raw):
        """Identify the meter of some input.

        :param raw: an input string
        """
        verse = Verse(raw)
        verse_scan = ''.join(verse.scan)

        for vrtta in self.vrttas:
            if vrtta.regex.match(verse_scan):
                return vrtta
            if vrtta.partial_regex.match(verse_scan):
                return vrtta

        totals = set()
        total = 0
        for L in verse_scan:
            if L == 'L':
                total += 1
            else:
                total += 2
            totals.add(total)
        for jati in self.jatis:
            # `x` is the running sums up to the end of pada `x`
            a, b, c, d = jati.counts
            b += a
            c += b
            d += c
            if a in totals:
                if b in totals and c in totals:
                    if d in totals or d - 1 in totals:
                        return jati

                # Must consider both paths -> no elif
                if b - 1 in totals and c - 1 in totals:
                    if d - 1 in totals or d - 2 in totals:
                        return jati

        return None
