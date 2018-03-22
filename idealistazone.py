from urllib.request import urlopen
from pyquery import PyQuery as pq

def getProvince():
	pagina = pq(urlopen("https://www.idealista.it/").read())
	province = []
	for li in pagina("#location-combo > li").items():
		if li.text() == "--":
			break
		province.append(li.text())
	#self.province = {}
	#self.province_c['value'] = sorted(province)

def getComuni(provincia):
	#self.provincia = event.widget.get()
	pagina = pq(urlopen("https://www.idealista.it/vendita-case/"+provincia.lower().replace(" ", "-").replace("'","")+"/comuni").read())
	#self.comuni = {}
	comuni = []
	for li in pagina("#location_list > li").items():
		for li_interno in li("ul > li").items():
			comuni.append(li_interno("a").text())
	#self.comuni_c["value"] = sorted(comuni)

def getZoneLocalita(comune,provincia):
	#self.comune = event.widget.get()
	pagina = pq(urlopen("https://www.idealista.it/vendita-case/"+comune.lower().replace(" ", "-").replace("'","")+"-"+provincia.lower().replace(" ", "-").replace("'","")+"/").read())
	#self.zone = {}
	zone = []
	for li in pagina(".breadcrumb-subitems > ul")("li").items():
		if li("strong").text() == comune:
			for li_interno in li("ul > li").items():
				zone.append(li_interno("a").text())
	print(zone)
	#self.zone_localita_c["value"] = sorted(zone)
