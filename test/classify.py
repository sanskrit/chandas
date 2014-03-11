# -*- coding: utf-8 -*-

import os

import pytest

from chandas.classify import Classifier
from chandas.wrappers import Line


@pytest.fixture(scope='session')
def full_classifier():
    test_dir = os.path.dirname(__file__)
    project_dir = os.path.dirname(test_dir)
    json_path = os.path.join(project_dir, 'data', 'data.json')
    return Classifier.from_json_file(json_path)


@pytest.fixture
def classify(full_classifier):
    """Helper fixture for testing a block."""
    def tester(data):
        return full_classifier.classify(data).name
    return tester


@pytest.fixture
def classify_line(full_classifier):
    """Helper fixture for testing a line."""
    def tester(data):
        return full_classifier.classify_lines(data)[0][1].name
    return tester


@pytest.fixture
def megh_1_1():
    return """
        kaScit kAntAvirahaguruRA svADikArapramattaH
        zApenAstaMgamitamahimA varzaBogyeRa BartuH .
        yakSazcakre janakatanayAsnAnapuRyodakezu
        snigDacCAyAtaruzu vasatiM rAmagiryASramezu .. 1 ..
        """


@pytest.fixture
def kale_arya():
    return """
        yenAmandamarande daladaravinde dinAnyanAyizata .
        kuwaje Kalu tenehA tenehA maDukareRa kaTam ..
        """


def test_init():
    classifier = Classifier()
    assert classifier.vrttas == []
    assert classifier.jatis == []


def test_samavrtta(classify, megh_1_1):
    assert classify(megh_1_1) == u'mandākrāntā'


def test_ardhasamavrtta(classify):
    data = """
        muravErivapustanutAM mudaM
        hemaniBAMSukacaMdanaliptam .
        gaganaM capalAmilitaM yaTA
        SAradanIraDarErupacitram ..
        """
    assert classify(data) == u'upacitra'


def test_vishamavrtta(classify):
    data = """
        aTa vAsavasya vacanena ruciravadanastrilocanam .
        klAMtirahitamaBirADayituM viDivattapAMsi vidaDe DanaMjayaH ..
        """
    assert classify(data) == u'udgatā'


def test_shloka(classify):
    data = """
        vAgarTAviva saMpfktO vAgarTapratipattaye .
        jagataH pitarO vande pArvatIparameSvarO .. 1 ..
        """
    assert classify(data) == u'śloka'


def test_jati_laghu_laghu(classify):
    data = """
        yenAmandamarande daladaravinde dinAnyanAyizata .
        kuwaje Kalu tenehA tenehA maDukareRa kaTa ..
        """
    assert classify(data) == u'āryā'


def test_jati_laghu_guru(classify, kale_arya):
    data = kale_arya
    assert classify(data) == u'āryā'


def test_jati_guru_laghu(classify):
    data = """
        yenAmandamarande daladaravinde dinAnyanAyizatA .
        kuwaje Kalu tenehA tenehA maDukareRa kaTa ..
        """
    assert classify(data) == u'āryā'


def test_jati_guru_guru(classify):
    data = """
        yenAmandamarande daladaravinde dinAnyanAyizatA .
        kuwaje Kalu tenehA tenehA maDukareRa kaTam ..
        """
    assert classify(data) == u'āryā'


def test_jati_false_positive_pada_a(full_classifier):
    data = """
        yenAmandamarandale daravinde dinAnyanAyizata .
        kuwaje Kalu tenehA tenehA maDukareRa kaTam ..
        """
    assert full_classifier.classify(data) is None


def test_classify_line_samavrtta(classify_line):
    data = "snigDacCAyAtaruzu vasatiM rAmagiryASramezu"
    assert classify_line(data) == u'mandākrāntā'


def test_classify_line_ardhasamavrtta(classify_line):
    data = "muravErivapustanutAM mudaM hemaniBAMSukacaMdanaliptam"
    assert classify_line(data) == u'upacitra'


def test_classify_line_vishamavrtta(classify_line):
    data = ("aTa vAsavasya vacanena ruciravadanastrilocanam ."
        "klAMtirahitamaBirADayituM viDivattapAMsi vidaDe DanaMjayaH ..")
    assert classify_line(data) == u'udgatā'


def test_classify_line_shloka(classify_line):
    data = 'kekake kekakekeke'
    assert classify_line(data) == u'śloka'


def test_classify_line_unknown(full_classifier):
    data = 'ka'
    assert full_classifier.classify_lines(data)[0][1] is None


def test_split_into_padas_vrtta(full_classifier, megh_1_1):
    padya = full_classifier.classify(megh_1_1)
    expected = [Line(x) for x in megh_1_1.strip().splitlines() if x]
    actual = full_classifier.split_into_padas(megh_1_1, padya)
    assert len(expected) == len(actual)
    for e, a in zip(expected, actual):
        assert e.clean == a.clean


def test_split_into_padas_jati(full_classifier, kale_arya):
    padya = full_classifier.classify(kale_arya)
    expected = [Line('yenAmandamarande'),
                Line('daladaravinde dinAnyanAyizata .'),
                Line('kuwaje Kalu tenehA'),
                Line('tenehA maDukareRa kaTam ..')]
    actual = full_classifier.split_into_padas(kale_arya, padya)
    assert len(expected) == len(actual)
    for e, a in zip(expected, actual):
        assert e.clean == a.clean
