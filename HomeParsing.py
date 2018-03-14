from urllib.request import urlopen
from pyquery import PyQuery as pq
import tkinter as tk
from tkinter import ttk
from json import loads


class HomeParsing(object):
	def __init__(self):
		self.GenerateWindow()

	def GenerateWindow(self):
		top = tk.Tk()
		top.geometry("800x800")
		frame = ttk.Frame(top)
		cmb = ttk.Combobox(top, state = 'readonly')
		moduli = json.loads(open("moduli.json").read())
		for modulo in moduli:
			w = Label(top, text=modulo)
			cmb['values'] = ('Vendita', 'Affitto')
		cmb.pack()
		top.mainloop()

	def BuildLink(self,parameters,function):
		return function(parameters)

	def ExtractAnnunci(self,indirizzo,selettore,funzione):
		pagina_vergine = urlopen(indirizzo).read()
		pagina = pq(pagina_vergine)
		oggetto = pagina(selettore)
		lista = funzione(oggetto)
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
