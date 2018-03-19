from pyquery import PyQuery
def upperfirst(x):
    return x[0].upper() + x[1:]

def price(oggetto):
    return oggetto.text()[2:]

def sup(oggetto):
    numeri = len(oggetto("strong"))
    return oggetto("strong").eq(numeri-1).text()

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
    numeri = len(parametro("strong"))
    return parametro("strong").eq(-3).text()

def wc(parametro):
    numeri = len(parametro("strong"))
    return parametro("strong").eq(-2).text()

def auto(parametro):
    try:
        lista = parametro("dl.col-xs-12").text().split("\n")
        indice = lista.index("Box e posti auto")+1
        return lista[indice]
    except ValueError:
        return ""

def floor(parametro):
    try:
        lista = parametro("dl.col-xs-12").text().split("\n")
        indice = lista.index("Piano")+1
        return lista[indice]
    except ValueError:
        return ""

def cash(parametro):
    try:
        lista = parametro("dl.col-xs-12").text().split("\n")
        indice = lista.index("Spese condominio")+1
        elementi = lista[indice].split(" ")[1]
        return elementi.split("/")[0]
    except ValueError:
        return ""

def agency(nome):
    return nome.eq(0).text()

#DA QUA ESTRAZIONE ANNUNCI

def link(url):
    lista = []
    for a in url("a").items():
        lista.append(a.attr("href"))
    return lista


def next(pagina,indirizzo):
    bottone = pagina(".pull-right")("li")
    if bottone("a").eq(0).hasClass("disabled"):
        return False
    else:
        if "pag=" in indirizzo:
            this = indirizzo.split("=")
            this[-1] = int(this[-1])+1
            this[-1] = str(this[-1])
            return "=".join(this)

        else:
            return indirizzo+"&pag=2"










selettori = [".maps-address > span"]
selettori += [".maps-address > span"]
selettori += [".maps-address > span"]
selettori += [".features__price"]
selettori += [".block__features-anction > .feature-action__features"]
selettori += [".block__features-anction > .feature-action__features"]
selettori += [".block__features-anction > .feature-action__features"]
selettori += ["dl.col-xs-12"]
selettori += ["dl.col-xs-12"]
selettori += ["dl.col-xs-12"]
selettori += [".contact-data__name"]
funzioni = [geo,country,zone,price,sup,room,wc,auto,floor,cash,agency]
selettore = ".text-primary"
funzione = link
