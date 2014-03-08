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


def test_init():
    classifier = Classifier()
    assert classifier.vrttas == []
    assert classifier.jatis == []


def test_samavrtta(full_classifier):
    data = """
           kaScit kAntAvirahaguruRA svADikArapramattaH
           zApenAstaMgamitamahimA varzaBogyeRa BartuH .
           yakSazcakre janakatanayAsnAnapuRyodakezu
           snigDacCAyAtaruzu vasatiM rAmagiryASramezu .. 1 ..
           """
    assert full_classifier.classify(data).name == u'mandākrānta'


def test_samavrtta_partial(full_classifier):
    data = "snigDacCAyAtaruzu vasatiM rAmagiryASramezu"
    assert full_classifier.classify(data).name == u'mandākrānta'


def test_ardhasamavrtta(full_classifier):
    data = """
           muravErivapustanutAM mudaM
           hemaniBAMSukacaMdanaliptam .
           gaganaM capalAmilitaM yaTA
           SAradanIraDarErupacitram ..
           """
    assert full_classifier.classify(data).name == u'upacitram'


def test_ardhasamavrtta_partial(full_classifier):
    data = "muravErivapustanutAM mudaM hemaniBAMSukacaMdanaliptam"
    assert full_classifier.classify(data).name == u'upacitram'


def test_vishamavrtta(full_classifier):
    data = """
           aTa vAsavasya vacanena ruciravadanastrilocanam .
           klAMtirahitamaBirADayituM viDivattapAMsi vidaDe DanaMjayaH ..
           """
    assert full_classifier.classify(data).name == u'udgatā'


def test_shloka(full_classifier):
    data = """
           vAgarTAviva saMpfktO vAgarTapratipattaye .
           jagataH pitarO vande pArvatIparameSvarO .. 1 ..
           """
    assert full_classifier.classify(data).name == u'śloka'


def test_shloka_partial(full_classifier):
    data = 'kA' * 8
    assert full_classifier.classify(data).name == u'śloka'


def test_shloka_partial_false_positive(full_classifier):
    data = 'kA' * 9
    assert full_classifier.classify(data) is None


def test_jati_laghu_laghu(full_classifier):
    data = """
           yenAmandamarande daladaravinde dinAnyanAyizata .
           kuwaje Kalu tenehA tenehA maDukareRa kaTa ..
           """
    assert full_classifier.classify(data).name == u'āryā'


def test_jati_laghu_guru(full_classifier):
    data = """
           yenAmandamarande daladaravinde dinAnyanAyizata .
           kuwaje Kalu tenehA tenehA maDukareRa kaTam ..
           """
    assert full_classifier.classify(data).name == u'āryā'


def test_jati_guru_laghu(full_classifier):
    data = """
           yenAmandamarande daladaravinde dinAnyanAyizatA .
           kuwaje Kalu tenehA tenehA maDukareRa kaTa ..
           """
    assert full_classifier.classify(data).name == u'āryā'


def test_jati_guru_guru(full_classifier):
    data = """
           yenAmandamarande daladaravinde dinAnyanAyizatA .
           kuwaje Kalu tenehA tenehA maDukareRa kaTam ..
           """
    assert full_classifier.classify(data).name == u'āryā'


def test_jati_false_positive_pada_a(full_classifier):
    data = """
           yenAmandamarandale daravinde dinAnyanAyizata .
           kuwaje Kalu tenehA tenehA maDukareRa kaTam ..
           """
    assert full_classifier.classify(data) is None
