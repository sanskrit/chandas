# -*- coding: utf-8 -*-
"""
    chandas.enums
    ~~~~~~~~~~~~~

    Various enumerated data.

    :license: MIT and BSD
"""

class SLP:

    """Stores SLP1 letters."""

    #: Every sound in SLP1, excluding accents and nasality
    ALL = 'aAiIuUfFxXeEoOkKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSshMH'

    #: Short vowels. Short and long vowels have different impacts on
    #: syllable weight.
    SHORT_VOWELS = 'aiufx'

    #: Long vowels. Short and long vowels have different impacts on
    #: syllable weight.
    LONG_VOWELS = 'AIUFXeEoO'

    #: All vowels
    VOWELS = SHORT_VOWELS + LONG_VOWELS

    #: Consonants. This excludes ``'M'`` and ``'H'``
    CONSONANTS = 'kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSsh'


class Weights:

    """Stores syllable weights."""

    #: Denotes a heavy syllable ('guru')
    HEAVY = 'G'

    #: Denotes a light syllable ('laghu')
    LIGHT = 'L'

    #: Denotes an arbitrary syllable
    EITHER = '.'

    #: Maps a triplet of syllable weights to a traditional "gaṇa" name.
    #:
    #: These triplets have the mnemonic "yamātārājabhānasalagāḥ", where
    #: a consonant and the two weights after it denote the weight of
    #: the appropriate triplet. Thus "ya mā tā" -> 'LGG'. Note that
    #: laghu ('la') and guru ('gāḥ') are encoded as well.
    GANAS = {
        'LGG': 'y',
        'GGG': 'm',
        'GGL': 't',
        'GLG': 'r',
        'LGL': 'j',
        'GLL': 'B',
        'LLL': 'n',
        'LLG': 's',
    }
