from urllib.request import urlopen
from pyquery import PyQuery as pq
import tkinter as tk
from tkinter import ttk
from importlib import import_module
import json


class HomeParsing(object):
	def __init__(self):
		self.GenerateWindow()

	def GenerateWindow(self):
		top = tk.Tk()
		top.geometry("400x800")
		frame = ttk.Frame(top)
		moduli = json.loads(open("moduli.json").read())
		for modulo in moduli:
			modulo_py = import_module(modulo)
			modulo_l = ttk.Label(top, text=modulo+":", padding=[0,10,0,10], font='Arial 15 bold')
			modulo_l.pack()
			regioni_l = ttk.Label(top, text="Region:", padding = [0,0,0,10], font = 'Arial 10')
			regioni = ttk.Combobox(top, state = 'readonly')
			regioni['values'] = modulo_py.getRegioni()
			regioni.bind("<<ComboboxSelected>>", modulo_py.getProvince)
			province_l = ttk.Label(top, text="Provincia:", padding = [0,10,0,10], font = 'Arial 10')
			province = ttk.Combobox(top, state = 'readonly')
			province['values'] = []
			province.bind("<<ComboboxSelected>>", modulo_py.getProvince)
			comuni_l = ttk.Label(top, text="Comune:", padding = [0,10,0,10], font = 'Arial 10')
			comuni = ttk.Combobox(top, state = 'readonly')
			comuni['values'] = []
			comuni.bind("<<ComboboxSelected>>", modulo_py.getZoneLocalita)
			regioni_l.pack()
			regioni.pack()
			province_l.pack()
			province.pack()
			comuni_l.pack()
			comuni.pack()
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
