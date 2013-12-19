# -*- coding: utf-8 -*-

from chandas.classes import *


class MeterTest:
    short_v = 'aiufx'
    long_v = 'AIUFXeEoO'
    vowels = 'aAiIuUfFxXeEoO'
    consonants = 'kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSsh'

    def yes(self, *args):
        assert self.check(*args)

    def no(self, *args):
        assert not self.check(*args)

    def check(self, *args):
        """Return ``True`` or ``False``"""
        raise NotImplementedError


class TestLineClean(MeterTest):

    def check(self, raw, result):
        return Line(raw).clean == result

    def test_empty(self):
        self.yes('', '')

    def test_numbers(self):
        self.yes('1234567890', '')

    def test_punctuation(self):
        self.yes('!@#$%^&*()[]{}/=?+|,.<>', '')

    def test_unicode(self):
        self.yes('देवनागरी', '')

    def test_whitespace(self):
        self.yes(' \t\r\f\v\n', '')

    def test_plain(self):
        s = 'kaScitkAntAvirahaguruRAsvADikArapramattaH'
        self.yes(s, s)

    def test_mixed(self):
        self.yes('a1#  $%\t2bन!!c', 'abc')


class TestLineEndsWithLaghu(MeterTest):

    def check(self, raw):
        return Line(raw).ends_with_laghu

    def test_empty(self):
        self.no('')

    def test_short_vowels(self):
        for v in self.short_v:
            self.yes(v)

    def test_long_vowels(self):
        for v in self.long_v:
            self.no(v)

    def test_final_consonant(self):
        for v in self.short_v:
            for c in self.consonants:
                self.no(v + c)


class TestLineGana(MeterTest):

    def check(self, scanned, result):
        return Line(scan=scanned).gana == result

    def test_single_gana(self):
        yes = self.yes
        yes('LGG', 'y')
        yes('GGG', 'm')
        yes('GGL', 't')
        yes('GLG', 'r')
        yes('LGL', 'j')
        yes('GLL', 'B')
        yes('LLL', 'n')
        yes('LLG', 's')

    def test_laghu_guru(self):
        yes = self.yes
        yes('L', 'l')
        yes('G', 'g')
        yes('LL', 'll')
        yes('LG', 'lg')
        yes('GL', 'gl')
        yes('GG', 'gg')

    def test_long(self):
        yes = self.yes
        yes('LGLGGLLGLGLG', 'jtjr')  # vaṃśastham
        yes('GGGGLLLLLGGLGGLGG', 'mBnttgg')  # mandākrāntā
        yes('GGGLLGLGLLLGGGLGGLG', 'msjsttg')  # śārdūlavikrīḍita


class TestLineScan(MeterTest):

    def check(self, raw, result):
        return Line(raw).scan == result

    def test_empty(self):
        self.yes('', '')

    def test_consonant_without_vowels(self):
        self.yes('k', '')

    def test_short_vowels_light(self):
        yes = self.yes

        for v in self.short_v:
            # Plain
            yes(v, 'L')

            # Preceded by consonants
            yes('kr' + v, 'L')

    def test_short_vowels_heavy(self):
        yes = self.yes

        for v in self.short_v:
            # Followed by 'MH'
            yes(v + 'M', 'G')
            yes(v + 'H', 'G')

            # Followed by single consonant
            yes(v + 'm', 'G')

            # Followed by conjunct
            yes(v + 'rv', 'G')

            # Surrounded
            yes('kr' + v + 'H', 'G')
            yes('kr' + v + 'm', 'G')
            yes('kr' + v + 'rv', 'G')

    def test_long_vowels_heavy(self):
        yes = self.yes

        for v in self.long_v:
            # Plain
            yes(v, 'G')

            # Followed by 'MH'
            yes(v + 'H', 'G')
            yes(v + 'M', 'G')

            # Followed by consonants

            # Preceded by consonants
            yes('kr' + v, 'G')

            # Surrounded
            yes('kr' + v + 'H', 'G')
            yes('kr' + v + 'm', 'G')
            yes('kr' + v + 'rv', 'G')

    def test_words(self):
        yes = self.yes

        # Initial short vowel, light
        yes('hata', 'LL')
        yes('hatO', 'LG')
        yes('hataH', 'LG')
        yes('hatam', 'LG')

        # Initial short vowel, heavy (MH)
        yes('kaMsa', 'GL')
        yes('kaMsO', 'GG')
        yes('kaMsaH', 'GG')
        yes('kaMsam', 'GG')

        # Initial short vowel, heavy (conjunct)
        yes('sarpa', 'GL')
        yes('sarpO', 'GG')
        yes('sarpaH', 'GG')
        yes('sarpam', 'GG')

        # Initial long vowel
        yes('nAda', 'GL')
        yes('nAdO', 'GG')
        yes('nAdaH', 'GG')
        yes('nAdam', 'GG')

    def test_lines(self):
        token = 'kaScitkAntAvirahaguruRAsvADikArapramattaH'
        self.yes(token, 'GGGGLLLLLGGLGGLGG')


class TestStartsWithConjunct(MeterTest):

    def check(self, raw):
        return Line(raw).starts_with_conjunct

    def test_vowels(self):
        for v in self.vowels:
            self.no(v)

    def test_general(self):
        self.yes('pra')


class TestLineSyllables(MeterTest):

    def check(self, raw, result):
        return Line(raw).syllables == result.split()

    def test_empty(self):
        self.yes('', '')

    def test_consonant_without_vowels(self):
        self.yes('k', '')

    def test_single_final_vowel(self):
        for v in self.vowels:
            self.yes(v, v)
            self.yes('kr' + v, 'kr' + v)

    def test_single_vowel_with_consonant(self):
        for v in self.vowels:
            token = v + 'k'
            self.yes(token, token)

    def test_words(self):
        yes = self.yes
        yes('gamana', 'ga ma na')
        yes('cARUraH', 'cA RU raH')
        yes('haMsena', 'haM se na')
        yes('pradIpasya', 'pra dI pa sya')
        yes('kArtsnyam', 'kA rtsnyam')


class TestVerseScan:

    megh_1_1 = """
        kaScitkAntAvirahaguruRAsvADikArapramattaH
        SApenAstaMgamitamahimA varzaBogyeRa BartuH .
        yakzaScakre janakatanayAsnAnapuRyodakezu
        snigDacCAyAtaruzu vasatiM rAmagiryASramezu .. 1 ..
        """

    def test_scan(self):
        verse = Verse(self.megh_1_1)
        scan = ['GGGGLLLLLGGLGGLGG'] * 4
        scan[-1] = scan[-1][:-1] + 'L'
        assert verse.scan == scan
