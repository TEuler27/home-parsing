from pyquery import PyQuery as pq
import requests
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
	oggetto = pagina(".info-data")(".txt-bold").eq(0)
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
	return testo.text().replace("\n"," ").replace("|","-").replace('"','')

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
			if "?" in indirizzo:
				url_spezzato = indirizzo.split("?")
				url_spezzato2 = url_spezzato[0].split("-")
			else:
				url_spezzato2 = indirizzo.split("-")
			url_spezzato2[-1] = int(url_spezzato2[-1])+1
			url_spezzato2[-1] = str(url_spezzato2[-1])
			if "?" in indirizzo:
				url_spezzato[0] = "-".join(url_spezzato2)
				return "?".join(url_spezzato)
			else:
				return "-".join(url_spezzato2)
		else:
			if "?" in indirizzo:
				url_spezzato = indirizzo.split("?")
				url_spezzato[0] += "lista-2"
				return "?".join(url_spezzato)
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
		file = open("opzioni.json","r", encoding="utf-8")
		preferenze = json.loads(file.read())
		file.close()
		self.headers = preferenze["idealista-header"]

	def GenerateWindow(self):
		def show_menu(e):
			w = e.widget
			the_menu.entryconfigure("Incolla",
			command=lambda: w.event_generate("<<Paste>>"))
			the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)
		file = open("opzioni.json","r", encoding="utf-8")
		preferenze = json.loads(file.read())
		file.close()
		frame = self.root
		if len(preferenze["idealista-header"]) == 0:
			self.askHeader()
		for widget in frame.winfo_children():
			if widget.winfo_class() != "Menu":
				widget.destroy()
		modulo_l = ttk.Label(frame, text="Idealista:", padding=[0,10,0,10], font='Arial 15 bold')
		modulo_l.config(background="#d9d9d9")
		modulo_l.pack()
		ven_aff_l = ttk.Label(frame, text="Vendita/Affitto:", padding = [0,0,0,10], font = 'Arial 10')
		self.ven_aff_c = ttk.Combobox(frame, state = 'readonly')
		self.ven_aff_c['values'] = ["Vendita", "Affitto"]
		province_l = ttk.Label(frame, text="Provincia:", padding = [0,10,0,10], font = 'Arial 10')
		province_l.config(background="#d9d9d9")
		self.province_c = ttk.Combobox(frame, state = 'readonly')
		comuni_l = ttk.Label(frame, text="Comune:", padding = [0,10,0,10], font = 'Arial 10')
		comuni_l.config(background="#d9d9d9")
		self.comuni_c = ttk.Combobox(frame, state = 'readonly')
		self.comuni_c['values'] = []
		zone_localita_l = ttk.Label(frame, text="Zona/Località:", padding = [0,10,0,10], font = 'Arial 10')
		zone_localita_l.config(background="#d9d9d9")
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
		empty_l = ttk.Label(frame, text="", padding = [0,5,0,5])
		empty_l.config(background="#d9d9d9")
		empty_l.pack()
		button = ttk.Button(frame, text="Scarica", command = lambda: threading.Thread(target=self.Magia).start())
		button.pack()
		pers_tit_l = ttk.Label(frame, text="Ricerca personalizzata:", padding=[0,15,0,15], font='Arial 13 bold')
		pers_tit_l.config(background="#d9d9d9")
		pers_tit_l.pack()
		pers_l = ttk.Label(frame,wraplength=450, text="Per effettuare una ricerca personalizzata fate la ricerca su immobiliare.it e copiate il link della pagina con gli annunci trovati in questo campo.", padding=[0,10,0,10])
		pers_l.config(background="#d9d9d9")
		pers_l.pack()
		self.pers = ttk.Entry(frame)
		self.pers.pack()
		the_menu = Menu(frame, tearoff=0)
		the_menu.add_command(label="Incolla")
		self.pers.bind("<Button-3>", show_menu)
		empty_l = ttk.Label(frame, text="", padding = [0,5,0,5])
		empty_l.config(background="#d9d9d9")
		empty_l.pack()
		button_pers = ttk.Button(frame, text="Scarica", command = lambda: threading.Thread(target=self.MagiaPers).start())
		button_pers.pack()
		self.province_c['values'] = self.getProvince()

	def MagiaPers(self):
		session = requests.Session()
		file = open("opzioni.json","r", encoding="utf-8")
		preferenze = json.loads(file.read())
		file.close()
		session.headers.update(self.headers)
		link = self.pers.get()
		Hp = HomeParsing(1,self.root)
		Hp.setSession(session)
		lista = Hp.ExtractAnnunci(link,self.funzione,nextPage,"https://www.idealista.it")
		t = tk.Toplevel(self.root,background="#d9d9d9")
		t.geometry("350x80")
		label = ttk.Label(t,text="Scaricamento in corso dei dati, attendere prego",padding = [0,10,0,10])
		label.config(background="#d9d9d9")
		label.pack()
		self.bar = ttk.Progressbar(t,mode = 'determinate', length = "250", maximum = len(lista))
		self.bar.pack()
		nomefile = preferenze["path"]+"Idealista-"+time.strftime("%d-%m__%H-%M")+".csv"
		legenda = "Indirizzo|Prezzo|Superficie|Locali|Bagni|Box Auto|Piano|Ascensore|Spese condominiali|Agenzia immobiliare|Descrizione|URL"
		file = open(nomefile,"w", encoding="utf-8")
		file.write(legenda+"\n")
		file.close()
		for n in range(len(lista)):
			if n != 0:
				Hp.ExtractData(lista[n],nomefile,self.funzioni,lista[n-1])
			else:
				Hp.ExtractData(lista[n],nomefile,self.funzioni,False)
			self.bar.step()
		t.destroy()

	def Magia(self):
		session = requests.Session()
		file = open("opzioni.json","r", encoding="utf-8")
		preferenze = json.loads(file.read())
		file.close()
		session.headers.update(self.headers)
		link = self.BuildLink()
		if not link:
			return
		Hp = HomeParsing(1,self.root)
		Hp.setSession(session)
		lista = Hp.ExtractAnnunci(link,self.funzione,nextPage,"https://www.idealista.it")
		t = tk.Toplevel(self.root,background="#d9d9d9")
		t.geometry("350x80")
		label = ttk.Label(t,text="Scaricamento in corso dei dati, attendere prego",padding = [0,10,0,10])
		label.config(background="#d9d9d9")
		label.pack()
		self.bar = ttk.Progressbar(t,mode = 'determinate', length = "250", maximum = len(lista))
		self.bar.pack()
		nomefile = preferenze["path"]+"Idealista-"+time.strftime("%d-%m__%H-%M")+".csv"
		legenda = "Indirizzo|Prezzo|Superficie|Locali|Bagni|Box Auto|Piano|Ascensore|Spese condominiali|Agenzia immobiliare|Descrizione|URL"
		file = open(nomefile,"w", encoding="utf-8")
		file.write(legenda+"\n")
		file.close()
		for n in range(len(lista)):
			if n != 0:
				Hp.ExtractData(lista[n],nomefile,self.funzioni,lista[n-1])
			else:
				Hp.ExtractData(lista[n],nomefile,self.funzioni,False)
			self.bar.step()
		t.destroy()

	def getProvince(self):
		def restart():
			w.destroy()
		s = requests.Session()
		s.headers.update(self.headers)
		req = s.get("https://www.idealista.it/")
		if req.status_code == 403:
			w = tk.Toplevel(self.root)
			w.configure(background="#d9d9d9")
			w.title("Sblocco richiesto")
			w.geometry("350x150")
			label = ttk.Label(w,wraplength=300,text="Idealista ci ha negato l'accesso. Visita la home di idealista digitando l'indirizzo direttamente dalla barra dell'url del tuo browser preferito e clicca su \"non sono un robot\". Se non visualizzi il captcha svuota la cache e riprova.",padding = [0,10,0,10])
			label.config(background="#d9d9d9")
			label.pack()
			button = ttk.Button(w, text="Riparti", command = restart)
			button.pack()
			w.update()
			w.grab_set()
			self.root.wait_window(w)
			req = s.get("https://www.idealista.it/")
		pagina = pq(req.text)
		province = []
		for li in pagina("#location-combo > li").items():
			if li.text() == "--":
				break
			province.append(li.text())
		self.province_c.set("")
		self.comuni_c.set("")
		self.zone_localita_c.set("")
		return province

	def getComuni(self,event):
		def restart():
			w.destroy()
		self.provincia = event.widget.get()
		s = requests.Session()
		s.headers.update(self.headers)
		if "-" in self.provincia:
			req = s.get("https://www.idealista.it/vendita-case/"+self.provincia.lower().replace(" ", "-").replace("'","")+"/comuni")
			if req.status_code == 403:
				w = tk.Toplevel(self.root)
				w.configure(background="#d9d9d9")
				w.title("Sblocco richiesto")
				w.geometry("350x150")
				label = ttk.Label(w,wraplength=300,text="Idealista ci ha negato l'accesso. Visita la home di idealista digitando l'indirizzo direttamente dalla barra dell'url del tuo browser preferito e clicca su \"non sono un robot\". Se non visualizzi il captcha svuota la cache e riprova.",padding = [0,10,0,10])
				label.config(background="#d9d9d9")
				label.pack()
				button = ttk.Button(w, text="Riparti", command = restart)
				button.pack()
				w.update()
				w.grab_set()
				self.root.wait_window(w)
				req = s.get("https://www.idealista.it/vendita-case/"+self.provincia.lower().replace(" ", "-").replace("'","")+"/comuni")
			pagina = pq(req.text)
		else:
			req = s.get("https://www.idealista.it/vendita-case/"+self.provincia.lower().replace(" ", "-").replace("'","")+"-provincia/comuni")
			if req.status_code == 403:
				w = tk.Toplevel(self.root)
				w.configure(background="#d9d9d9")
				w.title("Sblocco richiesto")
				w.geometry("350x150")
				label = ttk.Label(w,wraplength=300,text="Idealista ci ha negato l'accesso. Visita la home di idealista digitando l'indirizzo direttamente dalla barra dell'url del tuo browser preferito e clicca su \"non sono un robot\". Se non visualizzi il captcha svuota la cache e riprova.",padding = [0,10,0,10])
				label.config(background="#d9d9d9")
				label.pack()
				button = ttk.Button(w, text="Riparti", command = restart)
				button.pack()
				w.update()
				w.grab_set()
				self.root.wait_window(w)
				req = s.get("https://www.idealista.it/vendita-case/"+self.provincia.lower().replace(" ", "-").replace("'","")+"-provincia/comuni")
			pagina = pq(req.text)
		#self.comuni = {}
		comuni = []
		for li in pagina("#location_list > li").items():
			for li_interno in li("ul > li").items():
				comuni.append(li_interno("a").text())
		self.comuni_c["value"] = sorted(comuni)
		self.comuni_c.set("")
		self.zone_localita_c.set("")

	def getZoneLocalita(self,event):
		def restart():
			w.destroy()
		self.comune = event.widget.get()
		s = requests.Session()
		s.headers.update(self.headers)
		req = s.get("https://www.idealista.it/vendita-case/"+self.comune.lower().replace(" ", "-").replace("'","")+"-"+self.provincia.lower().replace(" ", "-").replace("'","")+"/")
		if req.status_code == 403:
			w = tk.Toplevel(self.root)
			w.configure(background="#d9d9d9")
			w.title("Sblocco richiesto")
			w.geometry("350x150")
			label = ttk.Label(w,wraplength=300,text="Idealista ci ha negato l'accesso. Visita la home di idealista digitando l'indirizzo direttamente dalla barra dell'url del tuo browser preferito e clicca su \"non sono un robot\". Se non visualizzi il captcha svuota la cache e riprova.",padding = [0,10,0,10])
			label.config(background="#d9d9d9")
			label.pack()
			button = ttk.Button(w, text="Riparti", command = restart)
			button.pack()
			w.update()
			w.grab_set()
			self.root.wait_window(w)
			req = s.get("https://www.idealista.it/vendita-case/"+self.comune.lower().replace(" ", "-").replace("'","")+"-"+self.provincia.lower().replace(" ", "-").replace("'","")+"/")
		pagina = pq(req.text)
		zone = []
		for li in pagina(".breadcrumb-subitems > ul")("li").items():
			if li("strong").text() == self.comune:
				for li_interno in li("ul > li").items():
					zone.append(li_interno("a").text())
		if len(zone) != 0:
			self.zone_localita_c["value"] = sorted(zone)
			self.zone_localita_c.set("")
		else:
			self.zone_localita_c["value"] = []
			self.zone_localita_c.set("")

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

	def askHeader(self):
		def Salva():
			input_str = e.get()
			headers = input_str.split("\n")
			result = {}
			for header in headers:
				split = header.split(":")
				if len(header) == 0:
					continue
				if header[0] == ":":
					continue
				if split[0].lower() == "accept-encoding" or split[0].lower() == "referer" or split[0].lower() == "connection":
					continue
				join = ":".join(split[1:])
				result[split[0].strip(" ")] = join.strip(" ")
			file = open("opzioni.json","r", encoding="utf-8")
			preferenze = json.loads(file.read())
			file.close()
			preferenze["idealista-header"] = result
			self.headers = result
			file = open("opzioni.json","w", encoding="utf-8")
			file.write(json.dumps(preferenze))
			file.close()
			t.destroy()
		t = tk.Toplevel(self.root)
		t.configure(background="#d9d9d9")
		t.title("Idealista Header")
		t.geometry("500x250")
		label = ttk.Label(t,wraplength=450,text="E' la prima volta che utilizzi il modulo di idealista. Per poter proseguire apri il tuo browser preferito, clicca con il tasto destro in qualsiasi punto della pagina e seleziona la voce ispeziona (o analizza elemento). Apri la voce network (o rete) e a questo punto visita la home di idealista digitando l'indirizzo direttamente dalla barra. Seleziona la scheda relativa al file \"/\" (o a www.idealista.it). Apri la voce \"header richiesta\" e copia tutto il suo contenuto in questo campo di testo.",padding = [0,10,0,10])
		label.config(background="#d9d9d9")
		label.pack()
		e = ttk.Entry(t)
		e.pack()
		empty_l = ttk.Label(t,text="",padding = [0,5,0,5])
		empty_l.config(background="#d9d9d9")
		empty_l.pack()
		button = ttk.Button(t, text="Salva", command = Salva)
		button.pack()
		t.grab_set()
		self.root.wait_window(t)
