from pyquery import PyQuery as pq
from urllib import request
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import json
import time
from HomeParsing import *
import threading

def upperfirst(x):
	return x[0].upper() + x[1:]

def price(pagina):
	#qua metti il selettore
	oggetto = pagina(".features__price")
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
	#qua metti il selettore
	oggetto = pagina(".block__features-anction > .feature-action__features")
	numeri = len(oggetto("strong"))
	return oggetto("strong").eq(numeri-1).text().replace(".","")

def geo(pagina):
	#qua metti il selettore
	indirizzo = pagina(".maps-address > span")
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
	parametro = pagina(".block__features-anction > .feature-action__features")
	for li in parametro("li").items():
		if li("i").hasClass("rooms"):
			return li("strong").text()
	return ""

def wc(pagina):
	#qua metti il selettore
	parametro = pagina(".block__features-anction > .feature-action__features")
	for li in parametro("li").items():
		if li("i").hasClass("bathrooms"):
			return li("strong").text()
	return ""

def auto(pagina):
	#qua metti il selettore
	parametro = pagina("dl.col-xs-12")
	for table in parametro.items():
		lista = table.text().split("\n")
		if "Box e posti auto" in lista:
			indice = lista.index("Box e posti auto")+1
			return lista[indice]
	return ""


def floor(pagina):
	#qua metti il selettore
	parametro = pagina("dl.col-xs-12")
	for table in parametro.items():
		lista = table.text().split("\n")
		if "Piano" in lista:
			indice = lista.index("Piano")+1
			return lista[indice]
	return ""

def cash(pagina):
	#qua metti il selettore
	parametro = pagina("dl.col-xs-12")
	for table in parametro.items():
		lista = table.text().split("\n")
		if "Spese condominio" in lista:
			indice = lista.index("Spese condominio")+1
			elementi = lista[indice].split(" ")[1]
			return elementi.split("/")[0]
	return ""

def agency(pagina):
	#qua metti il selettore
	nome = pagina(".contact-data__name")
	return nome.eq(0).text().replace("|", " ")

def description(pagina):
	#qua metti il selettore
	testo = pagina(".description-text")
	return testo.text().replace("\n"," ").replace("|","-")

def links(pagina):
	#qua metti il selettore
	url = pagina(".text-primary")
	lista = []
	for a in url("a").items():
		href = a.attr("href")
		if "http" not in href:
			lista.append("https://www.immobiliare.it"+href)
		elif "agenzie_immobiliari" not in href:
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
		self.funzioni = [geo,country,zone,price,sup,room,wc,auto,floor,cash,agency,description]
		self.funzione = links
		self.bar = False

	def GenerateWindow(self):
		frame = self.root
		for widget in frame.winfo_children():
			if widget.winfo_class() != "Menu":
				widget.destroy()
		modulo_l = ttk.Label(frame, text="Immobiliare:", padding=[0,10,0,10], font='Arial 15 bold')
		modulo_l.pack()
		ven_aff_l = ttk.Label(frame, text="Vendita/Affitto:", padding = [0,0,0,10], font = 'Arial 10')
		self.ven_aff_c = ttk.Combobox(frame, state = 'readonly')
		self.ven_aff_c['values'] = ["Vendita", "Affitto"]
		regioni_l = ttk.Label(frame, text="Regioni:", padding = [0,10,0,10], font = 'Arial 10')
		self.regioni_c = ttk.Combobox(frame, state = 'readonly')
		self.regioni_c['values'] = self.regioni
		province_l = ttk.Label(frame, text="Provincia:", padding = [0,10,0,10], font = 'Arial 10')
		self.province_c = ttk.Combobox(frame, state = 'readonly')
		self.province_c['values'] = []
		comuni_l = ttk.Label(frame, text="Comune:", padding = [0,10,0,10], font = 'Arial 10')
		self.comuni_c = ttk.Combobox(frame, state = 'readonly')
		self.comuni_c['values'] = []
		zone_localita_l = ttk.Label(frame, text="Zona/Località:", padding = [0,10,0,10], font = 'Arial 10')
		self.zone_localita_c = ttk.Combobox(frame, state = 'readonly')
		self.zone_localita_c['values'] = []
		self.regioni_c.bind("<<ComboboxSelected>>", self.getProvince)
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
		regioni_l.pack()
		self.regioni_c.pack()
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
		file = open("opzioni.json","r", encoding="utf-8")
		preferenze = json.loads(file.read())
		file.close()
		nomefile = preferenze["path"]+"Immobiliare-"+time.strftime("%d-%m__%H-%M")+".csv"
		legenda = "Indirizzo|Citta|Zona|Prezzo|Superficie|Locali|Bagni|Box Auto|Piano|Spese condominiali|Agenzia immobiliare|Descrizione|URL"
		file = open(nomefile,"w", encoding="utf-8")
		file.write(legenda+"\n")
		file.close()
		for url in lista:
			Hp.ExtractData(url,nomefile,self.funzioni)
			self.bar.step()
		t.destroy()

	def getProvince(self,event):
		self.regione = event.widget.get()
		json_data = json.loads(request.urlopen("https://www.immobiliare.it/servicesV6/mapchart/cartineMapArea/regioni/"+self.regione.lower()[:3]+".json").read().decode('utf8'))
		self.province = {}
		province = []
		for provincia in json_data["area"]:
			if provincia["indexArea"] == 0:
				self.province[provincia["nome"]] = provincia["idProvincia"]
				province += [provincia["nome"]]
		self.province_c['value'] = sorted(province)

	def getComuni(self,event):
		self.provincia = event.widget.get()
		sigla = self.province[self.provincia]
		header ={"referer":"https://www.immobiliare.it/"}
		req =  request.Request("https://www.immobiliare.it/services/geography/getGeography.php?action=getComuniProvincia&idProvincia="+sigla, headers=header)
		json_data = json.loads(request.urlopen(req).read().decode("utf8"))
		self.comuni = {}
		comuni = []
		for comune in json_data["result"]:
			self.comuni[comune["nome"]] = {"idComune": comune["idComune"], "conZone": comune["conZone"], "conLocalita": comune["conLocalita"], "keyurl": comune["keyurl"]}
			comuni += [comune["nome"]]
		self.comuni_c["value"] = sorted(comuni)

	def getZoneLocalita(self,event):
		self.comune = event.widget.get()
		if self.comuni[self.comune]["conZone"]:
			idComune = self.comuni[self.comune]["idComune"]
			header ={"referer":"https://www.immobiliare.it/"}
			req =  request.Request("https://www.immobiliare.it/services/geography/getGeography.php?action=getMacrozoneComune&idComune="+idComune, headers=header)
			json_data = json.loads(request.urlopen(req).read().decode("utf8"))
			self.zone = {}
			zone = []
			for idZona in json_data["result"]:
				self.zone[json_data["result"][idZona]['macrozona_nome_sn']] = json_data["result"][idZona]['macrozona_keyurl']
				zone += [json_data["result"][idZona]['macrozona_nome_sn']]
			self.zone_localita_c["value"] = sorted(zone)
		"""if self.comuni[self.comune]["conLocalita"]:
			pagina = pq(request.urlopen("https://www.immobiliare.it/vendita-case/"+self.comuni[self.comune]["keyurl"].lower().replace("_","-")).read().decode("utf8"))
			self.localita = []
			for localita in pagina(".breadcrumb-list").items("a"):
				self.localita += [localita.text()]
			combobox["value"] = self.localita"""

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
