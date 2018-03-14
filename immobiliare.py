from pyquery import PyQuery as pq
from urllib import request
import json

class Immobiliare:

	def __init__(self):
		self.regioni = ["Valle D'Aosta","Lombardia","Piemonte","Liguria","Trentino Alto-Adige","Veneto","Friuli Venezia-Giulia","Emilia Romagna","Toscana","Marche","Lazio","Umbria","Abruzzo","Molise","Basilicata","Puglia","Campania","Calabria","Sicilia","Sardegna"]
		self.regione = ""
		self.provincia = ""
		self.province = {}
		self.comune = ""
		self.comuni = {}
		self.zone = {}
		self.localita = []

	def getProvince(self,event):
		self.regione = event.widget.get()
		json_data = json.loads(request.urlopen("https://www.immobiliare.it/servicesV6/mapchart/cartineMapArea/regioni/"+self.regione.lower()[:3]+".json").read().decode('utf8'))
		self.province = {}
		province = []
		for provincia in json_data["area"]:
			if provincia["indexArea"] == 0:
				self.province[provincia["nome"]] = provincia["idProvincia"]
				province += [provincia["nome"]]
		return province

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
		return comuni

	def getZoneLocalita(self,event):
		self.comune = event.widget.get()
		if self.comuni[self.comune]["conZone"]:
			idComune = self.comuni[comune]["idComune"]
			header ={"referer":"https://www.immobiliare.it/"}
			req =  request.Request("https://www.immobiliare.it/services/geography/getGeography.php?action=getMacrozoneComune&idComune="+idComune, headers=header)
			json_data = json.loads(request.urlopen(req).read().decode("utf8"))
			self.zone = {}
			zone = []
			for idZona in json_data["result"]:
				self.zone[json_data["result"][idZona]['macrozona_nome_sn']] = json_data["result"][idZona]['macrozona_keyurl']
				zone += [json_data["result"][idZona]['macrozona_nome_sn']]
			return zone
		if self.comuni[self.comune]["conLocalita"]:
			pagina = pq(request.urlopen("https://www.immobiliare.it/vendita-case/"+self.comuni[self.comune]["keyurl"].lower().replace("_","-")).read().decode("utf8"))
			self.localita = []
			for localita in pagina(".breadcrumb-list").items("a"):
				self.localita += [localita.text()]
			return self.localita
