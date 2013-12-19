# -*- coding: utf-8 -*-

import re


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


class Meter:

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


class Line(object):

    """Handles a single line of metrical text.

    This automatically cleans the raw input and makes sure that all of
    the line-related functions are using the right input.
    """

    def __init__(self, raw=None, **kw):
        self.raw = raw

        if 'scan' in kw:
            self._scan = kw['scan']

    @property
    def clean(self):
        """Return the raw input with all non-SLP1 tokens removed.

        That includes whitespace, too!
        """
        clean = re.sub('[^%s]+' % SLP.ALL, '', self.raw)
        return clean

    @property
    def ends_with_laghu(self):
        """Return whether the line ends with a light syllable."""
        return self.scan and self.scan[-1] == Meter.LIGHT

    @property
    def gana(self):
        """Return the gaṇas that compose this line.

        The result is returned as a string, with each letter denoting
        a gaṇa. The full alphabet used is ``'ymtrjBnslg'``, where ``'l'``
        denotes laghu and ``'g'`` denotes guru.
        """
        converter = Meter.GANAS
        gana = []
        n = 3
        for i in xrange(0, len(self.scan), n):
            triple = self.scan[i:i+n]
            # Hit: gana found
            # Miss: < 3 syllables, just append
            try:
                gana.append(converter[triple])
            except KeyError:
                gana.append(triple.lower())

        return ''.join(gana)

    @property
    def scan(self):
        """Return the metrical scan of the line.

        Line-final laghu vowels are scanned as laghu.
        """
        try:
            return self._scan
        except AttributeError:
            pass
        cons = SLP.CONSONANTS
        short_v = SLP.SHORT_VOWELS
        long_v = SLP.LONG_VOWELS
        vowel = SLP.VOWELS
        # Remove extra initial consonants (edge case)
        data = re.sub('^[%s]+' % cons, '', self.clean)
        # Handle final consonants (edge case)
        data = re.sub('[%s][MH%s]+$' % (vowel, cons), '_', data)
        # Long vowels
        data = re.sub('[%s][%sMH]*' % (long_v, cons), '_', data)
        # Short vowels with anusvara/visarga/conjunct
        data = re.sub('[%s]([MH]|[%s]){2,}' % (short_v, cons), '_', data)
        # Short vowels without conjunct
        data = re.sub('[%s][%s]*' % (short_v, cons), '.', data)
        # Convert to normal symbols
        data = data.replace('_', Meter.HEAVY).replace('.', Meter.LIGHT)

        self._scan = data
        return data

    @property
    def starts_with_conjunct(self):
        """Return whether the line starts with a consonant cluster."""
        return re.match('[%s]{2,}' % SLP.CONSONANTS, self.clean)

    @property
    def syllables(self):
        """Split the line into syllables.

        Each syllable ends with one of the following:

        - a vowel
        - the *visarga*
        - the *anusvāra*
        - a consonant (last syllable only)
        """
        items = re.findall('.*?[%s][MH]?' % SLP.VOWELS, self.clean)

        # Handle final consonants (edge case)
        tail = re.search('([%s]+$)' % SLP.CONSONANTS, self.clean)
        if items and tail:
            items[-1] += tail.group(1)

        self._syllables = items
        return items


class Verse(object):

    """Handles multiple lines of metrical text."""

    def __init__(self, raw):
        self.raw = raw

        clean_lines = [x for x in raw.strip().splitlines() if x]
        self.lines = [Line(x) for x in clean_lines]

    @property
    def scan(self):
        """Return the metrical scan of the verse.

        Pāda-final laghu is scanned as guru if the pāda is odd and the
        next line starts with a conjunct. If the pāda is even, the laghu
        is left as-is.
        """
        returned = []
        for i, x in enumerate(self.lines):
            try:
                next_is_conjunct = self.lines[i + 1].starts_with_conjunct
            except IndexError:
                next_is_conjunct = False

            odd_pada = i % 2 == 0
            if odd_pada and x.ends_with_laghu and next_is_conjunct:
                returned.append(x.scan[:-1] + Meter.HEAVY)
            else:
                returned.append(x.scan)

        return returned
