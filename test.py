from HomeParsing import *
from idealista import *

HP = HomeParsing(new = 1)
ID = Idealista("A")
HP.ExtractData("https://www.idealista.it/immobile/13347140/","prova.csv",ID.funzioni)
