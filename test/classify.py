# -*- coding: utf-8 -*-

import os

import pytest

from chandas.classify import Classifier


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


def test_init():
    classifier = Classifier()
    assert classifier.vrttas == []
    assert classifier.jatis == []


def test_samavrtta(classify):
    data = """
        kaScit kAntAvirahaguruRA svADikArapramattaH
        zApenAstaMgamitamahimA varzaBogyeRa BartuH .
        yakSazcakre janakatanayAsnAnapuRyodakezu
        snigDacCAyAtaruzu vasatiM rAmagiryASramezu .. 1 ..
        """
    assert classify(data) == u'mandākrāntā'


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


def test_jati_laghu_guru(classify):
    data = """
        yenAmandamarande daladaravinde dinAnyanAyizata .
        kuwaje Kalu tenehA tenehA maDukareRa kaTam ..
        """
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


def test_samavrtta_line(classify_line):
    data = "snigDacCAyAtaruzu vasatiM rAmagiryASramezu"
    assert classify_line(data) == u'mandākrāntā'


def test_ardhasamavrtta_line(classify_line):
    data = "muravErivapustanutAM mudaM hemaniBAMSukacaMdanaliptam"
    assert classify_line(data) == u'upacitra'


def test_vishamavrtta_line(classify_line):
    data = ("aTa vAsavasya vacanena ruciravadanastrilocanam ."
        "klAMtirahitamaBirADayituM viDivattapAMsi vidaDe DanaMjayaH ..")
    assert classify_line(data) == u'udgatā'


def test_shloka_line(classify_line):
    data = 'kekake kekakekeke'
    assert classify_line(data) == u'śloka'
