from pyquery import PyQuery as pq
from urllib import request
from tkinter import ttk
import json
from HomeParsing import *

class Immobiliare:

	def __init__(self):
		self.regioni = ["Valle D'Aosta","Lombardia","Piemonte","Liguria","Trentino Alto-Adige","Veneto","Friuli Venezia-Giulia","Emilia Romagna","Toscana","Marche","Lazio","Umbria","Abruzzo","Molise","Basilicata","Puglia","Campania","Calabria","Sicilia","Sardegna"]
		self.regione = ""
		self.provincia = ""
		self.province = {}
		self.comune = ""
		self.comuni = {}
		self.zona = ""
		self.zone = {}
		self.localita = []

	def GenerateWindow(self):
		frame = ttk.Frame(width="200", height="200")
		modulo_l = ttk.Label(frame, text="Immobiliare:", padding=[0,10,0,10], font='Arial 15 bold')
		modulo_l.pack()
		ven_aff_l = ttk.Label(frame, text="Vendita/Affitto:", padding = [0,0,0,10], font = 'Arial 10')
		self.ven_aff = ttk.Combobox(frame, state = 'readonly')
		self.ven_aff['values'] = ["Vendita", "Affitto"]
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
		frame.pack()
		regioni_l.pack()
		self.regioni_c.pack()
		province_l.pack()
		self.province_c.pack()
		comuni_l.pack()
		self.comuni_c.pack()
		zone_localita_l.pack()
		self.zone_localita_c.pack()
		ttk.Label(frame, text="", padding = [0,5,0,5]).pack()
		button = ttk.Button(frame, text="Scarica", command = self.Magia)
		button.pack()

	def Magia(self):
		link = self.BuildLink(self.ven_aff.get(),self.provincia,self.comune,self.zona)
		lista = HomeParsing.ExtractAnnunci(link,selettore,funzione,next)
		for url in lista:
			HomeParsing.ExtractData(url,"Immobiliare"+time.strftime("%d/%m")+".csv",selettori,funzioni)

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

	def BuildLink(self,ven_aff,provincia,comune,zona):
		link = "https://www.immobiliare.it/"
		if ven_aff == "Vendita":
			link += "vendita-case/"
		else:
			link += "affitto-case/"
		if comune != "":
			link += comune.lower()+"/"
			if zona != "":
				link += self.zone[zona]+"/"
			return link
		return link+provincia.lower().replace(" ","-")+"-provincia/"
