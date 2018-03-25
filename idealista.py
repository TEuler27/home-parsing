from pyquery import PyQuery as pq
from urllib import request
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import json
import time
from HomeParsing import *
import threading
import pandas as pd

def upperfirst(x):
	return x[0].upper() + x[1:]

def price(pagina):
	#qua metti il selettore
	oggetto = pagina(".info-data")(".txt-bold").eq(1)
	prezzo = oggetto.text()
	if "€" in prezzo:
		if "da" in prezzo:
			return prezzo
		if "al mese" in prezzo:
			return prezzo[2:-8].replace(".","")
		return prezzo.replace(".","")
	else:
		return prezzo

def sup(pagina):
	#qua metti il selettore
	oggetto = pagina(".info-features")
	for span in oggetto("span").items():
		if "m2" in span.text():
			return span("span").eq(1).text()
	return ""

def geo(pagina):
	#qua metti il selettore
	indirizzo = pagina("#headerMap")("ul > li")
	return upperfirst(indirizzo.text().split(",")[0])

def country(pagina):
	#qua metti il selettore
	indirizzo = pagina(".maps-address > span")
	return indirizzo.text().split(",")[-1].split("-")[0].lstrip()

def zone(pagina):
	#qua metti il selettore
	indirizzo = pagina(".maps-address > span")
	zona = indirizzo.text().split(",")[-1].split("-")
	if len(zona)==2:
		return zona[1].lstrip()
	else:
		return ""

def room(pagina):
	#qua metti il selettore
	oggetto = pagina(".info-features")
	for span in oggetto("span").items():
		if "locali" in span.text():
			return span("span").eq(1).text()
	return ""

def wc(pagina):
	#qua metti il selettore
	parametro = pagina("details-property_features")
	for li in parametro("ul > li").items():
		if "bagni" in li.text() or "bagno" in li.text():
			return li.text()[1]
	return ""

def auto(pagina):
	#qua metti il selettore
	parametro = pagina("details-property_features")
	for li in parametro("ul > li").items():
		if "Garage/posto auto" in li.text():
			return li.text()
	return ""


def floor(pagina):
	#qua metti il selettore
	oggetto = pagina(".info-features")
	for span in oggetto("span").items():
		if "piano" in span.text() or "Piano" in span.text():
			return span("span").text()
	return ""

def cash(pagina):
	#qua metti il selettore
	parametro = pagina("display-table_cell")
	for p in parametro("p").items():
		if "spese condominiali" in p.text():
			return p.text().split(" ")[0]
	return ""

def agency(pagina):
	#qua metti il selettore
	pagina(".professional-name")("p").remove()
	return pagina(".professional-name").text()

def description(pagina):
	#qua metti il selettore
	testo = pagina(".adCommentsLanguage")
	return testo.text().replace("\n"," ").replace("|","-")

def links(pagina):
	#qua metti il selettore
	url = pagina(".text-primary")
	lista = []
	for a in url("a").items():
		href = a.attr("href")
		if "http" in href:
			lista.append(href)
	return lista


def nextPage(pagina,indirizzo):
	bottone = pagina(".pull-right")("li")
	if bottone("a").eq(0).html()==None:
		return False
	if bottone("a").eq(0).hasClass("disabled"):
		return False
	else:
		if "pag=" in indirizzo:
			this = indirizzo.split("=")
			this[-1] = int(this[-1])+1
			this[-1] = str(this[-1])
			return "=".join(this)

		else:
			return indirizzo+"&pag=2"


class Idealista:

	def __init__(self,root):
		self.root = root
		self.provincia = ""
		self.comune = ""
		self.zona = ""
		self.ven_aff = ""
		self.funzioni = [geo,country,zone,price,sup,room,wc,auto,floor,cash,agency,description]
		self.funzione = links
		self.bar = False

	def GenerateWindow(self):
		frame = ttk.Frame(width="200", height="200")
		modulo_l = ttk.Label(frame, text="Idealista:", padding=[0,10,0,10], font='Arial 15 bold')
		modulo_l.pack()
		ven_aff_l = ttk.Label(frame, text="Vendita/Affitto:", padding = [0,0,0,10], font = 'Arial 10')
		self.ven_aff_c = ttk.Combobox(frame, state = 'readonly')
		self.ven_aff_c['values'] = ["Vendita", "Affitto"]
		province_l = ttk.Label(frame, text="Provincia:", padding = [0,10,0,10], font = 'Arial 10')
		self.province_c = ttk.Combobox(frame, state = 'readonly')
		self.province_c['values'] = self.getProvince()
		comuni_l = ttk.Label(frame, text="Comune:", padding = [0,10,0,10], font = 'Arial 10')
		self.comuni_c = ttk.Combobox(frame, state = 'readonly')
		self.comuni_c['values'] = []
		zone_localita_l = ttk.Label(frame, text="Zona/Località:", padding = [0,10,0,10], font = 'Arial 10')
		self.zone_localita_c = ttk.Combobox(frame, state = 'readonly')
		self.zone_localita_c['values'] = []
		self.province_c.bind("<<ComboboxSelected>>", self.getComuni)
		self.comuni_c.bind("<<ComboboxSelected>>", self.getZoneLocalita)
		def save_zona(event):
			self.zona = event.widget.get()
		self.zone_localita_c.bind("<<ComboboxSelected>>", save_zona)
		def save_ven_aff(event):
			self.ven_aff = event.widget.get()
		self.ven_aff_c.bind("<<ComboboxSelected>>", save_ven_aff)
		frame.pack()
		ven_aff_l.pack()
		self.ven_aff_c.pack()
		province_l.pack()
		self.province_c.pack()
		comuni_l.pack()
		self.comuni_c.pack()
		zone_localita_l.pack()
		self.zone_localita_c.pack()
		ttk.Label(frame, text="", padding = [0,5,0,5]).pack()
		button = ttk.Button(frame, text="Scarica", command = lambda: threading.Thread(target=self.Magia).start())
		button.pack()

	def Magia(self):
		link = self.BuildLink()
		print(link)
		if not link:
			return
		Hp = HomeParsing(1,self.root)
		lista = Hp.ExtractAnnunci(link,self.funzione,nextPage)
		t = tk.Toplevel(self.root)
		t.geometry("300x80")
		label = ttk.Label(t,text="Scaricamento in corso dei dati, attendere prego",padding = [0,10,0,10])
		label.pack()
		self.bar = ttk.Progressbar(t,mode = 'determinate', length = "250", maximum = len(lista))
		self.bar.pack()
		nomefile = "Idealista-"+time.strftime("%d-%m--%H:%M")+".csv"
		legenda = "Indirizzo|Citta|Zona|Prezzo|Superficie|Locali|Bagni|Box Auto|Piano|Spese condominiali|Agenzia immobiliare|Descrizione|URL"
		file = open(nomefile,"w")
		file.write(legenda+"\n")
		file.close()
		for url in lista:
			Hp.ExtractData(url,nomefile,self.funzioni)
			self.bar.step()
		label["text"] = "Sto eliminando i duplicati, attendere prego"
		self.bar["mode"] = "indeterminate"
		self.bar.start()
		df = pd.read_csv(nomefile, sep="|")
		df.drop_duplicates(subset=None, inplace=True)
		df.to_csv(nomefile, sep="|", index = False)
		t.destroy()

	def getProvince(self):
		pagina = pq(urlopen("https://www.idealista.it/").read())
		province = []
		for li in pagina("#location-combo > li").items():
			if li.text() == "--":
				break
			province.append(li.text())
		return province

	def getComuni(self,event):
		self.provincia = event.widget.get()
		print("https://www.idealista.it/vendita-case/"+self.provincia.lower().replace(" ", "-").replace("'","")+"/comuni")
		if "-" in self.provincia:
			pagina = pq(urlopen("https://www.idealista.it/vendita-case/"+self.provincia.lower().replace(" ", "-").replace("'","")+"/comuni").read())
		else:
			pagina = pq(urlopen("https://www.idealista.it/vendita-case/"+self.provincia.lower().replace(" ", "-").replace("'","")+"-provincia/comuni").read())
		#self.comuni = {}
		comuni = []
		for li in pagina("#location_list > li").items():
			for li_interno in li("ul > li").items():
				comuni.append(li_interno("a").text())
		self.comuni_c["value"] = sorted(comuni)

	def getZoneLocalita(self,event):
		self.comune = event.widget.get()
		pagina = pq(urlopen("https://www.idealista.it/vendita-case/"+self.comune.lower().replace(" ", "-").replace("'","")+"-"+self.provincia.lower().replace(" ", "-").replace("'","")+"/").read())
		zone = []
		for li in pagina(".breadcrumb-subitems > ul")("li").items():
			if li("strong").text() == self.comune:
				for li_interno in li("ul > li").items():
					zone.append(li_interno("a").text())
		self.zone_localita_c["value"] = sorted(zone)

	def BuildLink(self):
		if self.ven_aff == "":
			a = messagebox.showerror("Errore", "Alcuni dati sono mancanti")
			return False
		if self.provincia == "":
			messagebox.showerror("Errore", "Alcuni dati sono mancanti")
			return False
		link = "https://www.immobiliare.it/"
		if self.ven_aff == "Vendita":
			link += "vendita-case/"
		else:
			link += "affitto-case/"
		if self.comune != "":
			link += self.comune.lower().replace(" ", "-")+"/"
			if self.zona != "":
				link += self.zone[self.zona]+"/"
			return link+"?criterio=rilevanza"
		return link+self.provincia.lower().replace(" ","-")+"-provincia/?criterio=rilevanza"
