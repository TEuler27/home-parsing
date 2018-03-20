from urllib.request import urlopen
from pyquery import PyQuery as pq
import tkinter as tk
from tkinter import ttk
from importlib import import_module
import json
import functools


class HomeParsing(object):
	def __init__(self, new = 0, root = False):
		if root:
			self.root = root
		self.GenerateWindow(new)

	def GenerateWindow(self,new):
		if new == 0:
			self.root = tk.Tk()
			self.root.geometry("800x800")
			moduli = json.loads(open("moduli.json").read())
			for modulo in moduli:
				modulo_py = getattr(import_module(modulo.lower()), modulo)
				classe = modulo_py(self.root)
				classe.GenerateWindow()
			self.root.mainloop()

	def ExtractAnnunci(self,indirizzo,selettore,funzione,next):
		t = tk.Toplevel(self.root)
		t.geometry("300x80")
		ttk.Label(t,text="Scaricamento in corso, attendere prego",padding = [5,0,5,0]).pack()
		self.bar = ttk.Progressbar(t,mode = 'indeterminate', length = "250")
		self.bar.pack()
		self.bar.start()
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
		t.destroy()
		return lista

	def ExtractData(self,indirizzo,nome_doc,selettori,funzioni):
		pagina_vergine = urlopen(indirizzo).read()
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
