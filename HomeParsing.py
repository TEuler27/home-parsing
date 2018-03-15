from urllib.request import urlopen
from pyquery import PyQuery as pq

class HomeParsing(object):
	def __init__(self):
		pass

	def BuildLink(self,parameters,function):
		return function(parameters)

	def ExtractAnnunci(self,indirizzo,selettore,funzione,next):
		pagina_vergine = urlopen(indirizzo).read()
		pagina = pq(pagina_vergine)
		oggetto = pagina(selettore)
		lista = funzione(oggetto)
		while next(pagina,indirizzo) != False:
			indirizzo = next(pagina,indirizzo)
			pagina_vergine = urlopen(indirizzo).read()
			pagina = pq(pagina_vergine)
			oggetto = pagina(selettore)
			lista += funzione(oggetto)
		oggetto = pagina(selettore)
		lista += funzione(oggetto)
		return lista

	def ExtractData(self,indirizzo,nome_doc,selettori,funzioni):
		try:
			pagina_vergine = urlopen(indirizzo).read()
		except:
			print(indirizzo)
			return
		pagina = pq(pagina_vergine)
		dati = ""
		for i in range(len(selettori)):
			oggetto = pagina(selettori[i])
			dato = funzioni[i](oggetto)
			if(i == 0):
				dati = dato
			else:
				dati += "|" + dato
		file = open(nome_doc,"a")
		file.write(dati+"\n")
		file.close()
