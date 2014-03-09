from chandas import Classifier

classifier = Classifier.from_json_file('data/data.json')

data = [
    """
    kaScit kAntAvirahaguruRA svADikArapramattaH
    zApenAstaMgamitamahimA varzaBogyeRa BartuH .
    yakSazcakre janakatanayAsnAnapuRyodakezu
    snigDacCAyAtaruzu vasatiM rAmagiryASramezu .. 1 ..
    """,
    """
    muravErivapustanutAM mudaM
    hemaniBAMSukacaMdanaliptam .
    gaganaM capalAmilitaM yaTA
    SAradanIraDarErupacitram ..
    """,
    """
    aTa vAsavasya vacanena ruciravadanastrilocanam .
    klAMtirahitamaBirADayituM viDivattapAMsi vidaDe DanaMjayaH ..
    """,
    """
    vAgarTAviva saMpfktO vAgarTapratipattaye .
    jagataH pitarO vande pArvatIparameSvarO .. 1 ..
    """,
    """
    yenAmandamarande daladaravinde dinAnyanAyizata .
    kuwaje Kalu tenehA tenehA maDukareRa kaTam ..
    """
]

for i in range(300):
    for datum in data:
        classifier.classify(datum)
