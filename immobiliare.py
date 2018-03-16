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

	def getProvince(self,event,combobox):
		self.regione = event.widget.get()
		json_data = json.loads(request.urlopen("https://www.immobiliare.it/servicesV6/mapchart/cartineMapArea/regioni/"+self.regione.lower()[:3]+".json").read().decode('utf8'))
		self.province = {}
		province = []
		for provincia in json_data["area"]:
			if provincia["indexArea"] == 0:
				self.province[provincia["nome"]] = provincia["idProvincia"]
				province += [provincia["nome"]]
		combobox['value'] = province

	def getComuni(self,event,combobox):
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
		combobox["value"] = comuni

	def getZoneLocalita(self,event,combobox):
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
			combobox["value"] = zone
		"""if self.comuni[self.comune]["conLocalita"]:
			pagina = pq(request.urlopen("https://www.immobiliare.it/vendita-case/"+self.comuni[self.comune]["keyurl"].lower().replace("_","-")).read().decode("utf8"))
			self.localita = []
			for localita in pagina(".breadcrumb-list").items("a"):
				self.localita += [localita.text()]
			combobox["value"] = self.localita"""

	def BuildLink(self,ven_aff,provincia,comune,zona):
		link = "https://www.immobiliare.it/"
		if ven_aff == 0:
			link += "vendita-case/"
		else:
			link += "affitto-case/"
		if comune != "":
			link += comune.lower()+"/"
			if zona != "":
				link += self.zone[zona]+"/"
			return link
		return link+provincia.lower().replace(" ","-")+"-provincia/"
