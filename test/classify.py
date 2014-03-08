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
    classifier = Classifier([])
    assert classifier.vrttas == []


def test_samavrtta(full_classifier):
    data = """
           kaScit kAntAvirahaguruRA svADikArapramattaH
           zApenAstaMgamitamahimA varzaBogyeRa BartuH .
           yakSazcakre janakatanayAsnAnapuRyodakezu
           snigDacCAyAtaruzu vasatiM rAmagiryASramezu .. 1 ..
           """
    assert full_classifier.classify(data).name == u'mandākrānta'

