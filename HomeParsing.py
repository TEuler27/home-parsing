import requests
from pyquery import PyQuery as pq
import tkinter as tk
from tkinter import Menu, ttk, filedialog
from importlib import import_module
import json
import functools
import datetime


class HomeParsing(object):
	def __init__(self, new = 0, root = False):
		if root:
			self.root = root
		self.GenerateWindow(new)

	def setSession(self,s):
		self.s = s

	def GenerateWindow(self,new):
		if new == 0:
			self.root = tk.Tk()
			self.root.configure(background="#d9d9d9")
			self.root.title("HomeParsing")
			self.root.geometry("500x400")
			menubar = Menu(self.root, relief="flat", bd = 2)
			filemenu = Menu(menubar, tearoff=0)
			moduli = json.loads(open("moduli.json").read())
			file = open("opzioni.json","r", encoding="utf-8")
			preferenze = json.loads(file.read())
			file.close()
			for modulo in moduli:
				modulo_py = getattr(import_module(modulo.lower()), modulo)
				classe = modulo_py(self.root)
				filemenu.add_command(label=modulo, command=classe.GenerateWindow)
				if modulo == preferenze["default"]:
					classe.GenerateWindow()
			menubar.add_cascade(label="Modulo", menu=filemenu)
			filemenu = Menu(menubar, tearoff=0)
			filemenu.add_command(label="Preferenze",command=self.Opzioni)
			menubar.add_cascade(label="Opzioni", menu=filemenu)
			self.root.config(menu=menubar)
			self.root.mainloop()

	def Opzioni(self):
		filename = ""
		def Path():
			nonlocal filename
			filename = filedialog.askdirectory()
			opzioni.lift()
			opzioni.attributes("-topmost", True)
			path_attuale["text"] = filename
		def Salva():
			default = default_c.get()
			file = open("opzioni.json","r", encoding="utf-8")
			preferenze = json.loads(file.read())
			file.close()
			preferenze["default"] = default
			if filename != "":
				preferenze["path"] = filename+"/"
			file = open("opzioni.json","w", encoding="utf-8")
			file.write(json.dumps(preferenze))
			file.close()
			opzioni.destroy()
		file = open("opzioni.json","r", encoding="utf-8")
		preferenze = json.loads(file.read())
		file.close()
		opzioni = tk.Tk()
		opzioni.configure(background="#d9d9d9")
		opzioni.title("Opzioni")
		opzioni.geometry("400x250")
		default_l = ttk.Label(opzioni, text="Modulo di apertura:", padding = [0,10,0,10], font = 'Arial 10')
		default_l.config(background="#d9d9d9")
		default_c = ttk.Combobox(opzioni, state = 'readonly')
		default_c['values'] = json.loads(open("moduli.json").read())
		default_c.current(default_c["values"].index(preferenze["default"]))
		empty_l = ttk.Label(opzioni, padding = [0,20,0,20])
		empty_l.config(background="#d9d9d9")
		path_l = ttk.Label(opzioni, text="Cartella di destinazione:", padding = [0,10,0,10], font = 'Arial 10')
		path_l.config(background="#d9d9d9")
		if preferenze["path"] == "":
			path_attuale = ttk.Label(opzioni, text="Stessa cartella del programma", padding = [0,0,0,10], font = 'Arial 10')
		else:
			path_attuale = ttk.Label(opzioni, text=preferenze["path"], padding = [0,0,0,10], font = 'Arial 10')
		path_attuale.configure(background="#d9d9d9")
		path_b = ttk.Button(opzioni, text="Sfoglia...", command = Path)
		default_l.pack()
		default_c.pack()
		path_l.pack()
		path_attuale.pack()
		path_b.pack()
		empty_l.pack()
		button = ttk.Button(opzioni, text="Salva", command = Salva)
		button.pack()

	def ExtractAnnunci(self,indirizzo,funzione,next,referer):
		def restart():
			w.destroy()
		indirizzo_start = indirizzo
		t = tk.Toplevel(self.root)
		t.configure(background="#d9d9d9")
		t.geometry("350x80")
		label1 = ttk.Label(t,text="Sto caricando gli annunci, attendere prego",padding = [0,10,0,10])
		label1.configure(background="#d9d9d9")
		label1.pack()
		self.bar = ttk.Progressbar(t,mode = 'indeterminate', length = "250")
		self.bar.pack()
		self.bar.start()
		req = self.s.get(indirizzo)
		pagina_vergine = req.text
		pagina = pq(pagina_vergine)
		lista = funzione(pagina)
		while next(pagina,indirizzo) != False:
			indirizzo_n = next(pagina,indirizzo)
			self.s.headers.update({"referer": indirizzo})
			req = self.s.get(indirizzo_n)
			if req.status_code == 403 and "idealista" in indirizzo_n:
				w = tk.Toplevel(self.root)
				w.configure(background="#d9d9d9")
				w.title("Sblocco richiesto")
				w.geometry("350x150")
				label2 = ttk.Label(w,wraplength=300,text="Idealista ci ha negato l'accesso. Visita la home di idealista digitando l'indirizzo direttamente dalla barra dell'url del tuo browser preferito e clicca su \"non sono un robot\". Se non visualizzi il captcha svuota la cache e riprova.",padding = [0,10,0,10])
				label2.configure(background="#d9d9d9")
				label2.pack()
				button = ttk.Button(w, text="Riparti", command = restart)
				button.pack()
				w.update()
				w.grab_set()
				self.root.wait_window(w)
				continue
			pagina_vergine = req.text
			pagina = pq(pagina_vergine)
			lista += funzione(pagina)
			indirizzo = indirizzo_n
		t.destroy()
		return lista

	def ExtractData(self,indirizzo,nome_doc,funzioni, referer, data = False):
		if data:
			time_data = datetime.datetime.strptime(data, "%d/%m/%Y").timestamp()
		def restart():
			w.destroy()
		if not referer:
			self.s.headers.update({"referer": "https://www.idealista.it"})
			req = self.s.get(indirizzo)
		else:
			self.s.headers.update({"referer": referer})
			req = self.s.get(indirizzo)
		if req.status_code == 403 and "idealista" in indirizzo:
			w = tk.Toplevel(self.root)
			w.configure(background="#d9d9d9")
			w.title("Sblocco richiesto")
			w.geometry("350x150")
			label = ttk.Label(w,wraplength=300,text="Idealista ci ha negato l'accesso. Visita la home di idealista digitando l'indirizzo direttamente dalla barra dell'url del tuo browser preferito e clicca su \"non sono un robot\". Se non visualizzi il captcha svuota la cache e riprova.",padding = [0,10,0,10])
			label.config(background="#d9d9d9")
			label.pack()
			button = ttk.Button(w, text="Riparti", command = restart)
			button.pack()
			w.update()
			w.grab_set()
			self.root.wait_window(w)
			req = self.s.get(indirizzo)
		pagina_vergine = req.text
		if ".casa" in indirizzo and "Ops... pagina non trovata" in pagina_vergine:
			self.ExtractData(indirizzo,nome_doc,funzioni, referer, data)
			return
		if "tecnocasa" in indirizzo and req.status_code == 404:
			return
		pagina = pq(pagina_vergine)
		dati = ""
		for i in range(len(funzioni)):
			dato = funzioni[i](pagina)
			if (i == 0):
				if not data:
					dati = dato
				else:
					time_ann = datetime.datetime.strptime(dato, "%d/%m/%Y").timestamp()
					if time_ann >= time_data:
						dati = dato
					else:
						return
			else:
				dati += "|" + dato
		dati += "|" + indirizzo
		file = open(nome_doc,"a",errors='ignore')
		file.write(dati+"\n")
		file.close()
