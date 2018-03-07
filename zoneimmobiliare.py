from pyquery import PyQuery as pq
from urllib import request
import json

class ZoneImmobiliare(object):

	def __init__(self):
		self.zone = {"Lombardia" : {}}

	def getProvince(self):
		for regione in self.zone:
			json_data = json.loads(request.urlopen("https://www.immobiliare.it/servicesV6/mapchart/cartineMapArea/regioni/"+regione.lower()[:3]+".json").read().decode('utf8'))
			for provincia in json_data["area"]:
				self.zone[regione][provincia["nome"]] = {"sigla": provincia["idProvincia"]}

	def getComuni(self):
		for regione in self.zone:
			for provincia in self.zone[regione]:
				sigla = self.zone[regione][provincia]["sigla"]
				header ={"referer":"https://www.immobiliare.it/"}
				req =  request.Request("https://www.immobiliare.it/services/geography/getGeography.php?action=getComuniProvincia&idProvincia="+sigla, headers=header)
				json_data = json.loads(request.urlopen(req).read().decode("utf8"))
				for comune in json_data["result"]:
					self.zone[regione][provincia][comune["nome"]] = {"conZone": comune["conZone"],"conLocalita": comune["conLocalita"], "idComune": comune["idComune"]}
