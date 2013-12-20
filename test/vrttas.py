from chandas.vrttas import *

class TestSamavrtta(object):

    name = 'mandAkrAntA'
    pattern = ['GGGGLLLLLGGLGGLGG']
    pada_scan = pattern * 4

    def test_init(self):
        v = Samavrtta(self.name, self.pattern)
        assert v.name == self.name
        assert v.pada_scan[0] == self.pattern[0]
        assert v.pada_scan == self.pada_scan

    def test_init_with_spaces(self):
        v = Samavrtta(self.name, ['G G G G | L L L L L G | G L G G L G G'])
        assert v.name == self.name
        assert v.pada_scan[0] == self.pattern[0]
        assert v.pada_scan == self.pada_scan
