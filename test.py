from HomeParsing import *

HP = HomeParsing()
HP.ExtractData("https://www.immobiliare.it/64359554-Vendita-Bilocale-via-Baioni-Monza.html","prova.csv",[".features__price"],[lambda x: x.text()])
