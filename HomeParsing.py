from urllib.request import urlopen
from pyquery import PyQuery as pq
import tkinter as tk
from tkinter import ttk
from importlib import import_module
import json
import functools


class HomeParsing(object):
	def __init__(self):
		self.GenerateWindow()

	def GenerateWindow(self):
		top = tk.Tk()
		top.geometry("400x800")
		frame = ttk.Frame(top)
		moduli = json.loads(open("moduli.json").read())
		button = ttk.Button(text="Scarica")
		for modulo in moduli:
			modulo_py = getattr(import_module(modulo.lower()), modulo)
			classe = modulo_py()
			modulo_l = ttk.Label(top, text=modulo+":", padding=[0,10,0,10], font='Arial 15 bold')
			modulo_l.pack()
			regioni_l = ttk.Label(top, name=modulo.lower()+"_regioni" , text="Regioni:", padding = [0,0,0,10], font = 'Arial 10')
			regioni = ttk.Combobox(top, state = 'readonly')
			regioni['values'] = classe.regioni
			province_l = ttk.Label(top, name=modulo.lower()+"_province", text="Provincia:", padding = [0,10,0,10], font = 'Arial 10')
			province = ttk.Combobox(top, state = 'readonly')
			province['values'] = []
			comuni_l = ttk.Label(top, name=modulo.lower()+"_comuni", text="Comune:", padding = [0,10,0,10], font = 'Arial 10')
			comuni = ttk.Combobox(top, state = 'readonly')
			comuni['values'] = []
			zone_localita_l = ttk.Label(top, name=modulo.lower()+"_zone_localita", text="Zona/Località:", padding = [0,10,0,10], font = 'Arial 10')
			zone_localita = ttk.Combobox(top, state = 'readonly')
			zone_localita['values'] = []
			regioni.bind("<<ComboboxSelected>>", functools.partial(classe.getProvince,combobox = province))
			province.bind("<<ComboboxSelected>>", functools.partial(classe.getComuni,combobox = comuni))
			comuni.bind("<<ComboboxSelected>>", functools.partial(classe.getZoneLocalita, combobox = zone_localita))
			button.bind('<Button-1>', lambda : for link in self.ExtractAnnunci(classe.BuildLink(0,province.get(),comuni.get(),zone_localita.get()),classe.selettore,classe.funzione): self.ExtractData(self,link,modulo.lower()+".csv",classe.selettori,classe.funzioni))
			regioni_l.pack()
			regioni.pack()
			province_l.pack()
			province.pack()
			comuni_l.pack()
			comuni.pack()
			zone_localita_l.pack()
			zone_localita.pack()
		top.mainloop()

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
