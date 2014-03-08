from chandas.vrttas import *


class TestVrtta(object):

    def test_clean(self):
        assert Vrtta._clean('LGLGL') == 'LGLGL'
        assert Vrtta._clean('L G L G L') == 'LGLGL'
        assert Vrtta._clean('L @#(*$)@ G | L G L') == 'LGLGL'


class TestSamavrtta(object):

    name = 'mandAkrAntA'
    pattern = ['GGGGLLLLLGGLGGLGG']

    def test_init(self):
        v = Samavrtta(self.name, self.pattern)
        assert v.name == self.name
        assert v.pada_scan[:1] == self.pattern
        assert v.pada_scan == self.pattern * 4


class TestArdhasamavrtta(object):

    name = 'viyoginI'
    pattern = ['LLGLLGLGLG', 'LLGGLLGLGLG']

    def test_init(self):
        v = Ardhasamavrtta(self.name, self.pattern)
        assert v.name == self.name
        assert v.pada_scan[:2] == self.pattern
        assert v.pada_scan == self.pattern * 2


class TestVishamavrtta(object):

    name = 'udgatA'
    pattern = ['LLGLGLLLGL', 'LLLLLGLGLG', 'GLLLLLLGLLG', 'LLGLGLLLGLGLG']
    pada_scan = pattern

    def test_init(self):
        v = Vishamavrtta(self.name, self.pattern)
        assert v.name == self.name
        assert v.pada_scan == self.pattern
        assert v.pada_scan == self.pada_scan
