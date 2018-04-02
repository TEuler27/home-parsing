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
	if "da" in prezzo:
		return prezzo
	if "al mese" in prezzo:
		return prezzo[2:-8].replace(".","")
	return prezzo.replace(".","")

def sup(pagina):
	#qua metti il selettore
	oggetto = pagina(".info-features")
	for span in oggetto("span").items():
		if "m2" in span.text():
			return span("span").eq(1).text()
	return ""

def geo(pagina):
	#qua metti il selettore
	indirizzo = pagina("#headerMap")("ul")
	return upperfirst(indirizzo.text().replace("\n","/"))

def room(pagina):
	#qua metti il selettore
	oggetto = pagina(".info-features")
	for span in oggetto("span").items():
		if "locali" in span.text() or "locale"in span.text():
			return span("span").eq(1).text()
	return ""

def wc(pagina):
	#qua metti il selettore
	parametro = pagina(".details-property_features")
	for li in parametro("ul > li").items():
		if "bagni" in li.text() or "bagno" in li.text():
			return li.text().split(" ")[0]
	return ""

def auto(pagina):
	#qua metti il selettore
	parametro = pagina(".details-property_features")
	for li in parametro("ul > li").items():
		if "Garage/posto auto" in li.text():
			return li.text()
	return ""


def floor(pagina):
	#qua metti il selettore
	oggetto = pagina(".info-features")
	for span in oggetto("span").items():
		if "piano" in span.text() or "Piano" in span.text():
			return span.text()
	return ""

def lift(pagina):
	frase = pagina(".details-property_features")
	for li in frase("ul > li").items():
		if "Con ascensore" in li.text():
			return "Si"
	return ""


def cash(pagina):
	#qua metti il selettore
	parametro = pagina(".display-table_cell")
	for p in parametro("p").items():
		if "spese condominiali" in p.text():
			return p.text().split(" ")[0]
	return ""

def agency(pagina):
	#qua metti il selettore
	pagina(".professional-name")("p").remove()
	return pagina(".professional-name").text().replace("\n"," ")

def description(pagina):
	#qua metti il selettore
	testo = pagina(".adCommentsLanguage")
	return testo.text().replace("\n"," ").replace("|","-")

def links(pagina):
	#qua metti il selettore
	url = pagina(".item-link")
	lista = []
	for a in url.items():
		href = a.attr("href")
		if "http" not in href:
			lista.append("https://www.idealista.it"+href)
		else:
			lista.append(href)
	return lista


def nextPage(pagina,indirizzo):
	bottone = pagina(".next > a.icon-arrow-right-after")
	if bottone.html()==None:
		return False
	else:
		if "lista-" in indirizzo:
			url_spezzato = indirizzo[0:-4].split("-")
			url_spezzato[-1] = int(url_spezzato[-1])+1
			url_spezzato[-1] = str(url_spezzato[-1])
			return "-".join(url_spezzato)+".htm"

		else:
			return indirizzo+"lista-2.htm"


class Idealista:

	def __init__(self,root):
		self.root = root
		self.provincia = ""
		self.comune = ""
		self.zona = ""
		self.ven_aff = ""
		self.funzioni = [geo,price,sup,room,wc,auto,floor,lift,cash,agency,description]
		self.funzione = links
		self.bar = False

	def GenerateWindow(self):
		frame = self.root
		for widget in frame.winfo_children():
			if widget.winfo_class() != "Menu":
				widget.destroy()
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
		file = open("opzioni.json","r")
		preferenze = json.loads(file.read())
		file.close()
		nomefile = preferenze["path"]+"Idealista-"+time.strftime("%d-%m--%H:%M")+".csv"
		legenda = "Indirizzo|Prezzo|Superficie|Locali|Bagni|Box Auto|Piano|Ascensore|Spese condominiali|Agenzia immobiliare|Descrizione|URL"
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
		req = request.Request("https://www.idealista.it/",headers={'User-Agent': 'Mozilla/5.0'})
		pagina = pq(urlopen(req).read())
		province = []
		for li in pagina("#location-combo > li").items():
			if li.text() == "--":
				break
			province.append(li.text())
		return province

	def getComuni(self,event):
		self.provincia = event.widget.get()
		if "-" in self.provincia:
			req = request.Request("https://www.idealista.it/vendita-case/"+self.provincia.lower().replace(" ", "-").replace("'","")+"/comuni",headers={'User-Agent': 'Mozilla/5.0'})
			pagina = pq(urlopen(req).read())
		else:
			req = request.Request("https://www.idealista.it/vendita-case/"+self.provincia.lower().replace(" ", "-").replace("'","")+"-provincia/comuni",headers={'User-Agent': 'Mozilla/5.0'})
			pagina = pq(urlopen(req).read())
		#self.comuni = {}
		comuni = []
		for li in pagina("#location_list > li").items():
			for li_interno in li("ul > li").items():
				comuni.append(li_interno("a").text())
		self.comuni_c["value"] = sorted(comuni)

	def getZoneLocalita(self,event):
		self.comune = event.widget.get()
		req = request.Request("https://www.idealista.it/vendita-case/"+self.comune.lower().replace(" ", "-").replace("'","")+"-"+self.provincia.lower().replace(" ", "-").replace("'","")+"/",headers={'User-Agent': 'Mozilla/5.0'})
		pagina = pq(urlopen(req).read())
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
		link = "https://www.idealista.it/"
		if self.ven_aff == "Vendita":
			link += "vendita-case/"
		else:
			link += "affitto-case/"
		if self.comune != "" and self.zona == "":
			return link+self.comune.lower().replace(" ", "-")+"-"+self.provincia.lower().replace(" ","-")+"/"
		if self.zona != "":
			return link+self.comune.lower().replace(" ", "-")+"/"+self.zona.lower().replace(" ","-")+"/"
		if "-" in self.provincia:
			return link+self.provincia.lower().replace(" ","-")+"/"
		else:
			return link+self.provincia.lower().replace(" ","-")+"-provincia/"
