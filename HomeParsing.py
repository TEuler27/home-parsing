from urllib.request import urlopen
from pyquery import PyQuery as pq
import tkinter as tk
from tkinter import Menu
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
			self.root.geometry("400x400")
			menubar = Menu(self.root, relief="flat", bd = 2)
			filemenu = Menu(menubar, tearoff=0)
			moduli = json.loads(open("moduli.json").read())
			for modulo in moduli:
				modulo_py = getattr(import_module(modulo.lower()), modulo)
				classe = modulo_py(self.root)
				filemenu.add_command(label=modulo, command=classe.GenerateWindow)
			menubar.add_cascade(label="Modulo", menu=filemenu)
			filemenu = Menu(menubar, tearoff=0)
			filemenu.add_command(label="Preferenze",command=self.Opzioni)
			menubar.add_cascade(label="Opzioni", menu=filemenu)
			self.root.config(menu=menubar)
			self.root.mainloop()

	def Opzioni(self):
		def Salva():
			default = default_c.get()
			file = open("opzioni.json","r")
			preferenze = json.loads(file.read())
			file.close()
			preferenze["default"] = default
			file = open("opzioni.json","w")
			file.write(json.dumps(preferenze))
			file.close()
			opzioni.destroy()
		file = open("opzioni.json","r")
		preferenze = json.loads(file.read())
		file.close()
		opzioni = tk.Tk()
		opzioni.title("Opzioni")
		opzioni.geometry("400x400")
		default_l = ttk.Label(opzioni, text="Modulo di apertura:", padding = [0,10,0,10], font = 'Arial 10')
		default_c = ttk.Combobox(opzioni, state = 'readonly')
		default_c['values'] = json.loads(open("moduli.json").read())
		default_c.current(default_c["values"].index(preferenze["default"]))
		default_l.pack()
		default_c.pack()
		button = ttk.Button(opzioni, text="Salva", command = Salva)
		button.pack()

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
