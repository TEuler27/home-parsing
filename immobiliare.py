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

def price(oggetto):
	return oggetto.text()[2:]

def sup(oggetto):
	numeri = len(oggetto("strong"))
	return oggetto("strong").eq(numeri-1).text()

def geo(indirizzo):
	return upperfirst(indirizzo.text().split(",")[0])

def country(indirizzo):
	return indirizzo.text().split(",")[-1].split("-")[0]

def zone(indirizzo):
	zona = indirizzo.text().split(",")[-1].split("-")
	if len(zona)==2:
		return zona[1]
	else:
		return ""

def room(parametro):
	numeri = len(parametro("strong"))
	return parametro("strong").eq(-3).text()

def wc(parametro):
	numeri = len(parametro("strong"))
	return parametro("strong").eq(-2).text()

def auto(parametro):
	try:
		lista = parametro("dl.col-xs-12").text().split("\n")
		indice = lista.index("Box e posti auto")+1
		return lista[indice]
	except ValueError:
		return ""

def floor(parametro):
	try:
		lista = parametro("dl.col-xs-12").text().split("\n")
		indice = lista.index("Piano")+1
		return lista[indice]
	except ValueError:
		return ""

def cash(parametro):
	try:
		lista = parametro("dl.col-xs-12").text().split("\n")
		indice = lista.index("Spese condominio")+1
		elementi = lista[indice].split(" ")[1]
		return elementi.split("/")[0]
	except ValueError:
		return ""

def agency(nome):
	return nome.eq(0).text()

#DA QUA ESTRAZIONE ANNUNCI

def links(url):
	lista = []
	for a in url("a").items():
		lista.append(a.attr("href"))
	return lista


def nextPage(pagina,indirizzo):
	bottone = pagina(".pull-right")("li")
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
		self.regioni = ["Valle D'Aosta","Lombardia","Piemonte","Liguria","Trentino Alto-Adige","Veneto","Friuli Venezia-Giulia","Emilia Romagna","Toscana","Marche","Lazio","Umbria","Abruzzo","Molise","Basilicata","Puglia","Campania","Calabria","Sicilia","Sardegna"]
		self.regione = ""
		self.provincia = ""
		self.province = {}
		self.comune = ""
		self.comuni = {}
		self.zona = ""
		self.zone = {}
		self.ven_aff = ""
		self.localita = []
		self.selettori = [".maps-address > span"]
		self.selettori += [".maps-address > span"]
		self.selettori += [".maps-address > span"]
		self.selettori += [".features__price"]
		self.selettori += [".block__features-anction > .feature-action__features"]
		self.selettori += [".block__features-anction > .feature-action__features"]
		self.selettori += [".block__features-anction > .feature-action__features"]
		self.selettori += ["dl.col-xs-12"]
		self.selettori += ["dl.col-xs-12"]
		self.selettori += ["dl.col-xs-12"]
		self.selettori += [".contact-data__name"]
		self.funzioni = [geo,country,zone,price,sup,room,wc,auto,floor,cash,agency]
		self.selettore = ".text-primary"
		self.funzione = links
		self.bar = False

	def GenerateWindow(self):
		frame = ttk.Frame(width="200", height="200")
		modulo_l = ttk.Label(frame, text="Immobiliare:", padding=[0,10,0,10], font='Arial 15 bold')
		modulo_l.pack()
		ven_aff_l = ttk.Label(frame, text="Vendita/Affitto:", padding = [0,0,0,10], font = 'Arial 10')
		self.ven_aff_c = ttk.Combobox(frame, state = 'readonly')
		self.ven_aff_c['values'] = ["Vendita", "Affitto"]
		regioni_l = ttk.Label(frame, text="Regioni:", padding = [0,0,0,10], font = 'Arial 10')
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
		frame.pack()
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
		print(link)
		if not link:
			return
		Hp = HomeParsing(1,self.root)
		lista = Hp.ExtractAnnunci(link,self.selettore,self.funzione,nextPage)
		t = tk.Toplevel(self.root)
		t.geometry("300x80")
		label = ttk.Label(t,text="Scaricamento in corso dei dati, attendere prego",padding = [0,10,0,10])
		label.pack()
		self.bar = ttk.Progressbar(t,mode = 'determinate', length = "250", maximum = len(lista))
		self.bar.pack()
		nomefile = "Immobiliare-"+time.strftime("%d-%m--%H:%M")+".csv"
		legenda = "Indirizzo|Citta|Zona|Prezzo|Superficie|Locali|Bagni|Box Auto|Piano|Spese condominiali|Agenzia immobiliare|Descrizione|URL"
		file = open(nomefile,"w")
		file.write(legenda+"\n")
		file.close()
		for url in lista:
			Hp.ExtractData(url,nomefile,self.selettori,self.funzioni)
			self.bar.step()
		label["text"] = "Sto eliminando i duplicati, attendere prego"
		self.bar["mode"] = "indeterminate"
		self.bar.start()
		df = pd.read_csv(nomefile, sep="|")
		df.drop_duplicates(subset=None, inplace=True)
		df.to_csv(nomefile, sep="|")
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
		self.province_c['value'] = province

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
		self.comuni_c["value"] = comuni

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
			self.zone_localita_c["value"] = zone
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
