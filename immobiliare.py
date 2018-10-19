from pyquery import PyQuery as pq
from urllib import request
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import json
import time
from HomeParsing import *
import threading
import requests

def upperfirst(x):
	if len(x) > 0:
		return x[0].upper() + x[1:]
	else:
		return ""

def price(pagina):

	oggetto = pagina(".features__price-block > .features__price")
	prezzo = oggetto.text()
	if "%" in prezzo:
		oggetto = pagina(".features__price-old--price")
		prezzo = oggetto.text()
	if "€" in prezzo:
		if "da" in prezzo:
			return prezzo
		if "al mese" in prezzo:
			return prezzo[2:-8].replace(".","")
		return prezzo[2:].replace(".","")
	else:
		return prezzo

def sup(pagina):

	oggetto = pagina(".features__list")
	numeri = oggetto(".features__only-text")
	return numeri(".text-bold").text()

def indirizzo(pagina):

	indirizzo = pagina(".pos-relative > span")
	if len(indirizzo) > 0:
		return upperfirst(indirizzo.text())
	else:
		indirizzo = pagina(".im-address__content")
		return upperfirst(indirizzo.text())

def room(pagina):

	parametro = pagina(".features__list")
	numeri = parametro("div")
	for oggetto in numeri:
		if numeri("span").hasClass("text-bold"):
			return numeri(".text-bold").text().split("&")[0][0]
		return ""
	return ""

def wc(pagina):

	parametro = pagina("dl.col-xs-12")
	for tag in parametro.items():
		lista = tag.text().split("\n")
		if "Locali" in lista:
			indice = lista.index("Locali")+1
			for elemento in lista[indice].split(","):
				if "bagn" in elemento:
					return elemento[1:2]
	return ""

def auto(pagina):

	parametro = pagina("dl.col-xs-12")
	for table in parametro.items():
		lista = table.text().split("\n")
		if "Box e posti auto" in lista:
			indice = lista.index("Box e posti auto")+1
			return lista[indice]
	return ""

def floor(pagina):

	parametro = pagina("dl.col-xs-12")
	for table in parametro.items():
		lista = table.text().split("\n")
		if "Piano" in lista:
			indice = lista.index("Piano")+1
			return lista[indice]
	return ""

def cash(pagina):

	parametro = pagina("dl.col-xs-12")
	for table in parametro.items():
		lista = table.text().split("\n")
		if "Spese condominio" in lista:
			indice = lista.index("Spese condominio")+1
			elementi = lista[indice].split(" ")[1]
			return elementi.split("/")[0]
	return ""

def agency(pagina):

	nome = pagina(".contact-data__name")
	return nome.eq(0).text().replace("|", " ")

def description(pagina):

	testo = pagina(".description-text")
	return testo.text().replace("\n"," ").replace("|","-").replace('"','')

def links(pagina):

	url = pagina(".text-primary")
	lista = []
	for a in url("a").items():
		href = a.attr("href")
		if "http" not in href:
			if "https://www.immobiliare.it"+href not in lista:
				lista.append("https://www.immobiliare.it"+href)
		elif "agenzie_immobiliari" not in href:
			if href not in lista:
				lista.append(href)
	return lista

def nextPage(pagina,indirizzo):
	bottone = pagina(".pull-right")("li")
	if bottone("a").eq(0).html()==None:
		print(pagina)
		return False
	if bottone("a").eq(0).hasClass("disabled"):
		return False
	else:
		return bottone("a").eq(0).attr("href")

def data(pagina):
	parametro = pagina("dl.col-xs-12")
	for table in parametro.items():
		lista = table.text().split("\n")
		if "Riferimento e Data annuncio" in lista:
			indice = lista.index("Riferimento e Data annuncio")+1
			if "-" in lista[indice]:
				elementi = lista[indice].split("-")[-1].strip()
			else:
				elementi = lista[indice].split(",")[-1].strip()
			return elementi
	return ""

class Immobiliare:

	def __init__(self,root):
		self.root = root
		self.regioni = sorted(["Valle D'Aosta","Lombardia","Piemonte","Liguria","Trentino Alto-Adige","Veneto","Friuli Venezia-Giulia","Emilia Romagna","Toscana","Marche","Lazio","Umbria","Abruzzo","Molise","Basilicata","Puglia","Campania","Calabria","Sicilia","Sardegna"])
		self.regione = ""
		self.provincia = ""
		self.province = {}
		self.comune = ""
		self.comuni = {}
		self.zona = ""
		self.zone = {}
		self.ven_aff = ""
		self.localita = []
		self.funzioni = [data,indirizzo,price,sup,room,wc,auto,floor,cash,agency,description]
		self.funzione = links
		self.bar = False

	def GenerateWindow(self):
		def show_menu(e):
			w = e.widget
			the_menu.entryconfigure("Incolla",
			command=lambda: w.event_generate("<<Paste>>"))
			the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)
		frame = self.root
		for widget in frame.winfo_children():
			if widget.winfo_class() != "Menu":
				widget.destroy()
		modulo_l = ttk.Label(frame, text="Immobiliare:", padding=[0,10,0,10], font='Arial 15 bold')
		modulo_l.config(background="#d9d9d9")
		modulo_l.pack()
		pers_tit_l = ttk.Label(frame, text="Ricerca personalizzata:", padding=[0,15,0,15], font='Arial 13 bold')
		pers_tit_l.config(background="#d9d9d9")
		pers_tit_l.pack()
		pers_l = ttk.Label(frame,wraplength=450, text="Per effettuare una ricerca personalizzata fate la ricerca su immobiliare.it e copiate il link della pagina con gli annunci trovati in questo campo.", padding=[0,10,0,10])
		pers_l.config(background="#d9d9d9")
		pers_l.pack()
		self.pers = ttk.Entry(frame)
		self.pers.pack()
		data_pers_l = ttk.Label(frame,wraplength=450, text="A partire dal (GG/MM/AAAA):", padding=[0,10,0,10])
		data_pers_l.config(background="#d9d9d9")
		data_pers_l.pack()
		self.data_pers = ttk.Entry(frame)
		self.data_pers.pack()
		the_menu = Menu(frame, tearoff=0)
		the_menu.add_command(label="Incolla")
		self.pers.bind("<Button-3>", show_menu)
		empty_l = ttk.Label(frame, text="", padding = [0,5,0,5])
		empty_l.config(background="#d9d9d9")
		empty_l.pack()
		button_pers = ttk.Button(frame, text="Scarica", command = lambda: threading.Thread(target=self.MagiaPers).start())
		button_pers.pack()

	def MagiaPers(self):
		session = requests.Session()
		link = self.pers.get()
		data = self.data_pers.get()
		Hp = HomeParsing(1,self.root)
		Hp.setSession(session)
		lista = Hp.ExtractAnnunci(link,self.funzione,nextPage,False)
		t = tk.Toplevel(self.root,background="#d9d9d9")
		t.geometry("350x80")
		label = ttk.Label(t,text="Scaricamento in corso dei dati, attendere prego",padding = [0,10,0,10])
		label.config(background="#d9d9d9")
		label.pack()
		self.bar = ttk.Progressbar(t,mode = 'determinate', length = "250", maximum = len(lista))
		self.bar.pack()
		file = open("opzioni.json","r", encoding="utf-8")
		preferenze = json.loads(file.read())
		file.close()
		nomefile = preferenze["path"]+"Immobiliare-"+time.strftime("%d-%m__%H-%M")+".csv"
		legenda = "Data annuncio|Indirizzo|Prezzo|Superficie|Locali|Bagni|Box Auto|Piano|Spese condominiali|Agenzia immobiliare|Descrizione|URL"
		file = open(nomefile,"w", encoding="utf-8")
		file.write(legenda+"\n")
		file.close()
		for url in lista:
			Hp.ExtractData(url,nomefile,self.funzioni,False,data)
			self.bar.step()
		t.destroy()
