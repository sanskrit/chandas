chandas
=======

Code to recognize various Sanskrit meters.

All of the hard work was done by the [sanskrit-programmers][thread] group,
especially the [first implementation][impl] by [shreevatsa][shreevatsa].
I've rewritten the code with a more streamlined API, and eventually I may
merge it into the [sanskrit][sanskrit] package.

The code supports any of the following metrical forms:

- *sama-vṛtta*
- *ardha-sama-vṛtta*
- *viṣama-vṛtta*
- *jāti*, including *āryā*

Quickstart
----------

    from chandas.classify import Classifier
    classifier = Classifier.from_json_file('data/data.json')

    result = classifier.classify('kaScit kAntAvirahaguruRA svADikArapramattaH')
    assert result and result.name == u'mandākrāntā'


Testing (requires [pytest][pytest])
-----------------------------------

    py.test test/*.py

To profile the code on some sample verses, run:

    python -m cProfile -s cumulative profile.py


Modules
-------

- `wrappers.py` for working with input data
- `padyas.py` for representing metrical forms
- `classify.py` for matching some input data with a metrical form
- `enums.py` for storing certain kinds of common data


[thread]: https://groups.google.com/forum/#!topic/sanskrit-programmers/8jhfDaawkWI
[impl]: https://github.com/shreevatsa/sanskrit/tree/metrical-scan
[shreevatsa]: https://github.com/shreevatsa
[sanskrit]: https://github.com/sanskrit/sanskrit
[pytest]: http://pytest.org/latest/


JSON format
-----------
A list of objects, each with these keys:

- `name`: the name of the meter. By default, all names are in lowercase IAST,
  but any representation is allowed.

- `pattern`: a list of syllable patterns. A pattern is just a string that uses
  the following characters.

  - `'G'` for *guru* syllables
  - `'L'` for *laghu* syllables
  - `'.'` for syllables that can be either *guru* or *laghu*
  - `'|'` for *yati*. (Currently, the package just ignores this.)

  All other characters in the pattern (including whitespace) are ignored.

  If the list has 1 pattern, then the verse is treated as *sama-vṛtta*. If the
  list has 2 patterns, then the verse is treated as *ardha-sama-vṛtta*. If the
  list has 4 patterns, then the verse is treated as *viṣama-vṛtta*.

- `counts`: **[optional]** for *jāti* meters. A list of 4 numbers, each denoting
  the *mātrā* length of the corresponding *pāda*.

  If this field is present, then the verse is treated as a *jāti* meter.

Examples:

    {
      "name": "mandākrāntā",
      "pattern": ["GGGG|LLLLLG|GLGGLGG"]
    },
    {
      "name": "upacitra",
      "pattern":["LLGLLGLLGLG", "GLLGLLGLLGG"]
    },
    {
      "name": "udgatā",
      "pattern": [
        "L L G L G L L L G L",
        "L L L L L G L G L G",
        "G L L L L L L G L L G",
        "L L G L G L L L G L G L G"
      ]
    },
    {
      "name": "āryā",
      "pattern": [],
      "counts": [12, 18, 12, 15]
    }
