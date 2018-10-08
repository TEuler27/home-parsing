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

	oggetto = pagina(".pinfo-price")
	if "Trattativa" in oggetto.text():
		return oggetto.text()
	prezzo = oggetto.text()[2:].replace(".","")
	if oggetto("a").html() != None:
		len_testo_eliminare = len(oggetto("a").text())
		prezzo = prezzo[:-len_testo_eliminare]
	if "al mese" in prezzo:
		return prezzo[:-8]
	else:
		return prezzo

def sup(pagina):

	oggetto = pagina(".mtq")
	return oggetto.text()

def indirizzo(pagina):

	indirizzo = pagina(".zone")
	return indirizzo.text()

def room(pagina):

	parametro = pagina(".pinfo-characteristics > li")
	numeri = parametro("span")
	for oggetto in numeri.items():
		if oggetto("i").hasClass("icon-locali"):
			return oggetto.text()
	return ""

def wc(pagina):

	parametro = pagina(".characteristics")
	for li in parametro("li").items():
		if "Bagni" in li.text():
			li("b").remove()
			return li.text()
	return ""


def auto(pagina):

	parametro = pagina(".characteristics")
	for li in parametro("li").items():
		if "Box" in li.text():
			li("b").remove()
			return li.text()
	return ""



def floor(pagina):

	parametro = pagina(".characteristics")
	for li in parametro("li").items():
		if "Piano" in li.text():
			li("b").remove()
			return li.text()
	return ""

def cash(pagina):

	parametro = pagina(".characteristics")
	for li in parametro("li").items():
		if "Spese Cond. Mese" in li.text():
			li("b").remove()
			return li.text()
	return ""

def agency(pagina):

	if "Privato" in pagina(".agency-info").text():
		return "Privato"
	else:
		return pagina(".name-agency").text().replace("|", " ")
	# link = pagina(".agency-info")("a").attr("href")
	# session = requests.Session()
	# if "http" not in link:
	# 	link = "https://www.casa.it" + link
	# pagina_nuova = pq(session.get(link).text)

def description(pagina):

	testo = pagina(".description")
	testo(".description-header").remove()
	return testo.text().replace("\n"," ").replace("|","-").replace('"','')

def links(pagina):

	url = pagina(".listing-list > li")
	lista = []
	for a in url("a").items():
		href = a.attr("href")
		if "http" not in href:
			if "https://www.casa.it"+href not in lista:
				lista.append("https://www.casa.it"+href)
	return lista


def nextPage(pagina,indirizzo):
	parti = indirizzo.split("?")
	splitted = parti[0].split("-")
	splitted[len(splitted)-1] = int(splitted[len(splitted)-1]) + 1
	splitted[len(splitted)-1] = str(splitted[len(splitted)-1])
	indirizzo_nuovo = "-".join(splitted)
	session = requests.Session()
	pagina_nuova = pq(session.get(indirizzo_nuovo).text)
	if pagina_nuova(".no-results").html() == None:
		return indirizzo_nuovo+"?"+parti[1]
	else:
		return False

def data(pagina):
	try:
		data_str = pagina(".last-mod").text()[14:]
		print(data_str)
		data_list = data_str.split(" ")
		giorno = data_list[0]
		if len(giorno) == 1:
			giorno = "0" + giorno
		mese = {
	        'Gennaio' : "01",
	        'Febbraio' : "02",
	        'Marzo' : "03",
	        'Aprile' : "04",
	        'Maggio' : "05",
	        'Giugno' : "06",
	        'Luglio' : "07",
	        'Agosto' : "08",
	        'Settembre' : "09",
	        'Ottobre' : "10",
	        'Novembre' : "11",
	        'Dicembre' : "12"
		}[data_list[1]]
		anno = data_list[2]
		return giorno+"/"+mese+"/"+anno
	except:
		return ""

class Casa:

	def __init__(self,root):
		self.root = root
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
		modulo_l = ttk.Label(frame, text="Casa.it:", padding=[0,10,0,10], font='Arial 15 bold')
		modulo_l.config(background="#d9d9d9")
		modulo_l.pack()
		pers_tit_l = ttk.Label(frame, text="Ricerca personalizzata:", padding=[0,15,0,15], font='Arial 13 bold')
		pers_tit_l.config(background="#d9d9d9")
		pers_tit_l.pack()
		pers_l = ttk.Label(frame,wraplength=450, text="Per effettuare una ricerca personalizzata fate la ricerca su casa.it e copiate il link della pagina con gli annunci trovati in questo campo.", padding=[0,10,0,10])
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
		print(len(lista))
		return None
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
		nomefile = preferenze["path"]+"Casa-"+time.strftime("%d-%m__%H-%M")+".csv"
		legenda = "Data annuncio|Zona|Prezzo|Superficie|Locali|Bagni|Box Auto|Piano|Spese condominiali|Agenzia immobiliare|Descrizione|URL"
		file = open(nomefile,"w", encoding="utf-8")
		file.write(legenda+"\n")
		file.close()
		for url in lista:
			print(url)
			Hp.ExtractData(url,nomefile,self.funzioni,False,data)
			self.bar.step()
		t.destroy()
