from HomeParsing import *
from idealista import *

HP = HomeParsing(new = 1)
ID = Idealista("A")
HP.ExtractData("https://www.idealista.it/immobile/13685379/","prova.csv",ID.funzioni)
