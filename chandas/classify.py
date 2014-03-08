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

            vrttas = []
            jatis = []
            for datum in data:
                len_pattern = len(datum['pattern'])
                if len_pattern == 1:
                    cls = Samavrtta
                elif len_pattern == 2:
                    cls = Ardhasamavrtta
                elif len_pattern == 4:
                    cls = Vishamavrtta
                elif datum.get('counts'):
                    cls = Jati

                padya = cls(**datum)
                if cls is Jati:
                    jatis.append(padya)
                else:
                    vrttas.append(padya)
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

        for vrtta in self.vrttas:
            if vrtta.num_syllables < len(verse_scan):
                continue
            if vrtta.partial_regex.match(verse_scan):
                if vrtta.num_syllables % len(verse_scan):
                    continue
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
