from HomeParsing import *
from immobiliare import *

HP = HomeParsing()
#HP.ExtractAnnunci("https://www.immobiliare.it/vendita-case/monza/?criterio=rilevanza&pag=110",selettore,funzione,next)
lista = HP.ExtractAnnunci("https://www.immobiliare.it/vendita-case/monza/?criterio=rilevanza",selettore,funzione,next)
for link in lista:
    HP.ExtractData(link,"prova.csv",selettori,funzioni)
