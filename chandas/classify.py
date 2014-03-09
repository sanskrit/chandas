# -*- coding: utf-8 -*-
"""
    chandas.classify
    ~~~~~~~~~~~~~~~~

    Top-level code for identifying the meter of some raw input.

    :license: MIT
"""

import json

from .enums import Weights
from .padyas import Ardhasamavrtta, Jati, Samavrtta, Vishamavrtta
from .wrappers import Block


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
                if datum.get('counts'):
                    cls = Jati
                elif len_pattern == 1:
                    cls = Samavrtta
                elif len_pattern == 2:
                    cls = Ardhasamavrtta
                elif len_pattern == 4:
                    cls = Vishamavrtta
                else:
                    raise NotImplementedError

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
        block = Block(raw)
        block_scan = ''.join(block.scan)

        # Vṛtta (entire block)
        # Exact regex match on the input scan.
        for vrtta in self.vrttas:
            if vrtta.regex.match(block_scan):
                return vrtta

        # Jāti (entire block)
        # Consider a *jāti* definition (a, b, c, d), where `a` denotes
        # the *mātrā* length of *pāda* A. To verify the input, we check
        # whether it is possible to divide the input into chunks of
        # length `a`, `b`, `c` and `d`.
        #
        # However, *pāda* B can be either `b` or `b - 1` long, and
        # likewise for *pāda* D.
        #
        # The algorithm first computes the *mātrā* length for all
        # `scan[:i]`. After that, it's O(1) to check whether the input
        # conforms to some *jāti*.
        totals = set()
        total = 0
        for syllable in block_scan:
            total += 1 if syllable == Weights.LIGHT else 2
            totals.add(total)
        for jati in self.jatis:
            # `x` is the running sum up to the end of pada `x`
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

        # Vṛtta (first pāda)
        for vrtta in self.vrttas:
            if vrtta.num_syllables < len(block_scan):
                continue
            if vrtta.partial_regex.match(block_scan):
                if vrtta.num_syllables % len(block_scan):
                    continue
                return vrtta
        return None
