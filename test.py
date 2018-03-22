from HomeParsing import *
from idealista import *

HP = HomeParsing(new = 1)
ID = Idealista("A")
HP.ExtractData("https://www.idealista.it/immobile/13810310/","prova.csv",ID.funzioni)
