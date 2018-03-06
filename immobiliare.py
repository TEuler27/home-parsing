#classe immobiliare con selettori e funzioni associate
from pyquery import PyQuery
def price(oggetto):
    return oggetto.text()[2:]

def sup(oggetto):
    return oggetto.text().split(" ")[0]

def geo(oggetto):
    return oggetto.text()

selettori = [".features__price"]
selettori += ["a[data-target='#consistenzeSuperficie']"]
selettori += [".maps-address > span"]
funzioni = [price,sup,geo]
