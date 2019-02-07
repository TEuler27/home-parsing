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

def empty(pagina):
	return ""

def tot_spese(pagina):
	return "=ARROTONDA(INDIRETTO(\"A\"&RIF.RIGA())+INDIRETTO(\"B\"&RIF.RIGA());2)"

def incasso(pagina):
	return "=ARROTONDA(INDIRETTO(\"D\"&RIF.RIGA())*INDIRETTO(\"L\"&RIF.RIGA());2)"

def utile(pagina):
	return "=ARROTONDA(INDIRETTO(\"E\"&RIF.RIGA())-INDIRETTO(\"C\"&RIF.RIGA());2)"

def stanze_utile(pagina):
	return "=ARROTONDA((INDIRETTO(\"G\"&RIF.RIGA())+INDIRETTO(\"C\"&RIF.RIGA()))/INDIRETTO(\"E\"&RIF.RIGA());2)"

def diff_locali(pagina):
	return "=ARROTONDA(INDIRETTO(\"H\"&RIF.RIGA())-INDIRETTO(\"L\"&RIF.RIGA());2)"

def affitto_mq(pagina):
	return "=ARROTONDA(INDIRETTO(\"A\"&RIF.RIGA())/INDIRETTO(\"K\"&RIF.RIGA());2)"

def costo_mq(pagina):
	return "=ARROTONDA(INDIRETTO(\"B\"&RIF.RIGA())/INDIRETTO(\"C\"&RIF.RIGA());2)"

def price(pagina):
	oggetto = pagina(".immobilePrezzo")
	if "Trattativa" in oggetto.text():
		return oggetto.text()
	prezzo = oggetto.text().split(" ")
	return prezzo[1].replace(".","")

def sup(pagina):
	oggetto = pagina(".schedaAnnuncioCampi > div")
	for div in oggetto.items():
		if "Superficie" in div.text():
			div("strong").remove()
			return div.text().split(" ")[2]
	return ""

def indirizzo(pagina):
	oggetto = pagina(".schedaAnnuncioCampi > div")
	for div in oggetto.items():
		if "Indirizzo" in div.text():
			div("strong").remove()
			return div.text()[2:]
	return ""

def room(pagina):
	oggetto = pagina(".schedaAnnuncioCampi > div")
	for div in oggetto.items():
		if "Locali" in div.text():
			div("strong").remove()
			return div.text()[2:]
	return ""

def wc(pagina):
	oggetto = pagina(".schedaAnnuncioCampi > div")
	for div in oggetto.items():
		if "Bagni" in div.text():
			div("strong").remove()
			return div.text()[2:]
	return ""

def auto(pagina):
	oggetto = pagina(".schedaAnnuncioCampi > div")
	for div in oggetto.items():
		if "Box" in div.text():
			return div.text()[-2:]
	return ""

def floor(pagina):
	parametro = pagina(".schedaAnnuncioCampi > div")
	for div in parametro.items():
		if "Piano" in div.text():
			div("strong").remove()
			return div.text()[2:]
	return ""

def cash(pagina):
	parametro = pagina(".schedaAnnuncioCampi > div")
	for div in parametro.items():
		if "Spese Annue" in div.text():
			div("strong").remove()
			spese_anno = div.text()[4:].replace(".","")
			return str(round(int(spese_anno)/12))
	return ""

def agency(pagina):
	parametro = pagina(".affiliato > div")
	nome = parametro("strong").text()
	return nome

def description(pagina):
	pagina(".CErow").remove()
	testo = pagina(".schedaAnnuncioDescrizione")
	return testo.text().replace("\n"," ").replace("|","-").replace('"','')

def links(pagina):
	url = pagina(".immobileLink")
	lista = []
	for a in url("a").items():
		href = a.attr("href")
		lista.append(href)
		if "http" not in href:
			if "https://www.tecnocasa.it"+href not in lista:
				lista.append("https://www.tecnocasa.it"+href)
	return lista

def nextPage(pagina,indirizzo):
	blocco = pagina(".pagination > li ")
	for li in blocco.items():
		if ">" in li.text():
			href = li("a").attr("href")
			return href
	return False

def data(pagina):
	return ""

class Tecnocasa:

	def __init__(self,root):
		self.root = root
		self.funzioni = [data,indirizzo,price,sup,room,wc,auto,floor,cash,agency,description]
		self.funzione = links
		self.funzioni_affitti = [price,cash,tot_spese,empty,incasso,utile,empty,stanze_utile,diff_locali,affitto_mq,sup,room,wc,floor,description]
		self.funzioni_acquisti = [indirizzo,price,sup,costo_mq,room,wc,auto,floor,cash,description]
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
		modulo_l = ttk.Label(frame, text="Tecnocasa:", padding=[0,10,0,10], font='Arial 15 bold')
		modulo_l.config(background="#d9d9d9")
		modulo_l.pack()
		pers_tit_l = ttk.Label(frame, text="Ricerca personalizzata:", padding=[0,15,0,15], font='Arial 13 bold')
		pers_tit_l.config(background="#d9d9d9")
		pers_tit_l.pack()
		self.type = tk.IntVar()
		ttk.Radiobutton(frame, text="Affitto", variable=self.type, value=0).pack()
		ttk.Radiobutton(frame, text="Vendita", variable=self.type, value=1).pack()
		pers_l = ttk.Label(frame,wraplength=450, text="Per effettuare una ricerca personalizzata fate la ricerca su casa.it e copiate il link della pagina con gli annunci trovati in questo campo.", padding=[0,10,0,10])
		pers_l.config(background="#d9d9d9")
		pers_l.pack()
		self.pers = ttk.Entry(frame)
		self.pers.pack()
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
		data = ""
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
		nomefile = preferenze["path"]+"Tecnocasa-"+time.strftime("%d-%m__%H-%M")+".csv"
		if self.type.get() == 0:
			legenda = "Affitto|Spese|Tot. Spese|Rivendita|Incasso|Utile|Utile voluto|Stanze per utile voluto|Differenza locali|Affitto mq|Superficie|Locali|Bagni|Piano|Zona|Descrizione|Link"
			funzioni = self.funzioni_affitti
		else:
			legenda = "Zona|Prezzo|Superficie|Costo mq|Locali|Bagni|Box Auto|Piano|Spese condominiali|Descrizione|URL"
			funzioni = self.funzioni_acquisti
		file = open(nomefile,"w", encoding="utf-8")
		file.write(legenda+"\n")
		file.close()
		for url in lista:
			print(url)
			Hp.ExtractData(url,nomefile,funzioni,False,data)
			self.bar.step()
		t.destroy()
