# -*- coding: utf-8 -*-

from chandas.wrappers import *


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

    def scan2raw(self, scan):
        return scan.replace('G', 'kA').replace('L', 'ka')


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
        raw = self.scan2raw(scanned)
        return Line(raw).gana == result

    def test_empty(self):
        self.yes('', '')

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


class TestLineMatraCount(MeterTest):

    def check(self, scanned, result):
        raw = self.scan2raw(scanned)
        return Line(raw).matra_count == result

    def test_empty(self):
        self.yes('', 0)

    def test_scan_single_syllable(self):
        yes = self.yes
        yes('L', 1)
        yes('G', 2)

    def test_scan_multiple(self):
        yes = self.yes
        yes('LL', 2)
        yes('LG', 3)
        yes('GL', 3)
        yes('GG', 4)

    def test_scan_long(self):
        self.yes('LLLLGLLGG', 12)


class TestLineScan(MeterTest):

    def func(self, raw):
        return Line(raw).scan

    def test_empty(self):
        assert self.func('') == ''

    def test_consonant_without_vowels(self):
        assert self.func('k') == ''

    def test_short_vowels_light(self):
        f = self.func
        for v in self.short_v:
            # Plain
            assert f(v) == 'L'

            # Preceded by consonants
            assert f('kr' + v) == 'L'

    def test_short_vowels_heavy(self):
        f = self.func
        for v in self.short_v:
            # Followed by 'MH'
            assert f(v + 'M') == 'G'
            assert f(v + 'H') == 'G'

            # Followed by single consonant
            assert f(v + 'm') == 'G'

            # Followed by conjunct
            assert f(v + 'rv') == 'G'

            # Surrounded
            assert f('kr' + v + 'H') == 'G'
            assert f('kr' + v + 'm') == 'G'
            assert f('kr' + v + 'rv') == 'G'

    def test_long_vowels_heavy(self):
        f = self.func
        for v in self.long_v:
            # Plain
            assert f(v) == 'G'

            # Followed by 'MH'
            assert f(v + 'H') == 'G'
            assert f(v + 'M') == 'G'

            # Followed by consonants

            # Preceded by consonants
            assert f('kr' + v) == 'G'

            # Surrounded
            assert f('kr' + v + 'H') == 'G'
            assert f('kr' + v + 'm') == 'G'
            assert f('kr' + v + 'rv') == 'G'

    def test_words(self):
        f = self.func

        # Initial short vowel, light
        assert f('hata') == 'LL'
        assert f('hatO') == 'LG'
        assert f('hataH') == 'LG'
        assert f('hatam') == 'LG'

        # Initial short vowel, heavy (MH)
        assert f('kaMsa') == 'GL'
        assert f('kaMsO') == 'GG'
        assert f('kaMsaH') == 'GG'
        assert f('kaMsam') == 'GG'

        # Initial short vowel, heavy (conjunct)
        assert f('sarpa') == 'GL'
        assert f('sarpO') == 'GG'
        assert f('sarpaH') == 'GG'
        assert f('sarpam') == 'GG'

        # Initial long vowel
        assert f('nAda') == 'GL'
        assert f('nAdO') == 'GG'
        assert f('nAdaH') == 'GG'
        assert f('nAdam') == 'GG'

    def test_lines(self):
        token = 'kaScitkAntAvirahaguruRAsvADikArapramattaH'
        assert self.func(token) == 'GGGGLLLLLGGLGGLGG'

    def test_bad_lines(self):
        assert self.func('taM iti') == 'LLL'
        assert self.func('naraH iti') == 'LLLL'


class TestLineStartsWithConjunct(MeterTest):

    def check(self, raw):
        return Line(raw).starts_with_conjunct

    def test_empty(self):
        self.no('')

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


class TestBlockScan(MeterTest):

    megh_1_1 = """
        kaScitkAntAvirahaguruRAsvADikArapramattaH
        SApenAstaMgamitamahimA varzaBogyeRa BartuH .
        yakzaScakre janakatanayAsnAnapuRyodakezu
        snigDacCAyAtaruzu vasatiM rAmagiryASramezu .. 1 ..
        """

    def check(self, raw, result):
        return Block(raw).scan == result

    def test_empty(self):
        self.yes('', [])

    def test_scan(self):
        scan = ['GGGGLLLLLGGLGGLGG'] * 4
        scan[-1] = scan[-1][:-1] + 'L'
        self.yes(self.megh_1_1, scan)
