#classe immobiliare con selettori e funzioni associate
from pyquery import PyQuery
def upperfirst(x):
    return x[0].upper() + x[1:]

def price(oggetto):
    return oggetto.text()[2:]

def sup(oggetto):
    return oggetto.text().split(" ")[0]

def geo(indirizzo):
    return upperfirst(indirizzo.text().split(",")[0])

def country(indirizzo):
    return indirizzo.text().split(",")[-1].split("-")[0]

def zone(indirizzo):
    zona = indirizzo.text().split(",")[-1].split("-")
    if len(zona)==2:
        return zona[1]
    else:
        return ""

def room(parametro):
    lista = parametro("dl.col-xs-12").text().split("\n")
    indice = lista.index("Locali")+1
    return lista[indice]

def auto(parametro):
    lista = parametro("dl.col-xs-12").text().split("\n")
    indice = lista.index("Box e posti auto")+1
    return lista[indice]

def floor(parametro):
    lista = parametro("dl.col-xs-12").text().split("\n")
    indice = lista.index("Piano")+1
    return lista[indice]

def cash(parametro):
    lista = parametro("dl.col-xs-12").text().split("\n")
    indice = lista.index("Spese condominio")+1
    return lista[indice]

def agency(nome):
    return nome.eq(0).text()


selettori = [".maps-address > span"]
selettori += [".maps-address > span"]
selettori += [".maps-address > span"]
selettori += [".features__price"]
selettori += ["a[data-target='#consistenzeSuperficie']"]
selettori += ["dl.col-xs-12"]
selettori += ["dl.col-xs-12"]
selettori += ["dl.col-xs-12"]
selettori += ["dl.col-xs-12"]
selettori += [".contact-data__name"]
funzioni = [geo,country,zone,price,sup,room,auto,floor,cash,agency]
