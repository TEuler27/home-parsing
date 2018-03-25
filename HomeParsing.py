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
			self.root.title("HomeParsing")
			self.root.geometry("800x800")
			moduli = json.loads(open("moduli.json").read())
			for modulo in moduli:
				modulo_py = getattr(import_module(modulo.lower()), modulo)
				classe = modulo_py(self.root)
				classe.GenerateWindow()
			self.root.mainloop()

	def ExtractAnnunci(self,indirizzo,funzione,next):
		t = tk.Toplevel(self.root)
		t.geometry("300x80")
		ttk.Label(t,text="Sto caricando gli annunci, attendere prego",padding = [0,10,0,10]).pack()
		self.bar = ttk.Progressbar(t,mode = 'indeterminate', length = "250")
		self.bar.pack()
		self.bar.start()
		pagina_vergine = urlopen(indirizzo).read()
		pagina = pq(pagina_vergine)
		lista = funzione(pagina)
		while next(pagina,indirizzo) != False:
			indirizzo = next(pagina,indirizzo)
			pagina_vergine = urlopen(indirizzo).read()
			pagina = pq(pagina_vergine)
			lista += funzione(pagina)
		lista += funzione(pagina)
		t.destroy()
		return lista

	def ExtractData(self,indirizzo,nome_doc,funzioni):
		print(indirizzo)
		try:
			pagina_vergine = urlopen(indirizzo).read()
		except:
			print(indirizzo)
			return
		pagina = pq(pagina_vergine)
		dati = ""
		for i in range(len(funzioni)):
			dato = funzioni[i](pagina)
			if(i == 0):
				dati = dato
			else:
				dati += "|" + dato
		dati += "|" + indirizzo
		file = open(nome_doc,"a")
		file.write(dati+"\n")
		file.close()
