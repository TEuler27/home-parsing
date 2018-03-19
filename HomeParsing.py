from urllib.request import urlopen
from pyquery import PyQuery as pq
import tkinter as tk
from importlib import import_module
import json
import functools


class HomeParsing(object):
	def __init__(self, new = 0):
		self.GenerateWindow(new)

	def GenerateWindow(self,new):
		if new == 0:
			root = tk.Tk()
			root.geometry("800x800")
			moduli = json.loads(open("moduli.json").read())
			for modulo in moduli:

				modulo_py = getattr(import_module(modulo.lower()), modulo)
				classe = modulo_py()
				classe.GenerateWindow()
			root.mainloop()

	def ExtractAnnunci(self,indirizzo,selettore,funzione,next):
		pagina_vergine = urlopen(indirizzo).read()
		pagina = pq(pagina_vergine)
		oggetto = pagina(selettore)
		lista = funzione(oggetto)
		while next(pagina,indirizzo) != False:
			try:
				print(indirizzo)
				indirizzo = next(pagina,indirizzo)
				pagina_vergine = urlopen(indirizzo).read()
				pagina = pq(pagina_vergine)
				oggetto = pagina(selettore)
				lista += funzione(oggetto)
			except:
				print(indirizzo)
		oggetto = pagina(selettore)
		lista += funzione(oggetto)
		return lista

	def ExtractData(self,indirizzo,nome_doc,selettori,funzioni):
		pagina_vergine = urlopen(indirizzo).read()
		pagina = pq(pagina_vergine)
		dati = ""
		print(indirizzo)
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
