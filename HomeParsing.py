from urllib import request
from pyquery import PyQuery as pq
import tkinter as tk
from tkinter import Menu, ttk, filedialog
from importlib import import_module
import json
import functools
from fake_useragent import UserAgent


class HomeParsing(object):
	def __init__(self, new = 0, root = False):
		if root:
			self.root = root
		self.GenerateWindow(new)

	def GenerateWindow(self,new):
		if new == 0:
			self.root = tk.Tk()
			self.root.title("HomeParsing")
			self.root.geometry("500x500")
			menubar = Menu(self.root, relief="flat", bd = 2)
			filemenu = Menu(menubar, tearoff=0)
			moduli = json.loads(open("moduli.json").read())
			file = open("opzioni.json","r", encoding="utf-8")
			preferenze = json.loads(file.read())
			file.close()
			for modulo in moduli:
				modulo_py = getattr(import_module(modulo.lower()), modulo)
				classe = modulo_py(self.root)
				filemenu.add_command(label=modulo, command=classe.GenerateWindow)
				if modulo == preferenze["default"]:
					classe.GenerateWindow()
			menubar.add_cascade(label="Modulo", menu=filemenu)
			filemenu = Menu(menubar, tearoff=0)
			filemenu.add_command(label="Preferenze",command=self.Opzioni)
			menubar.add_cascade(label="Opzioni", menu=filemenu)
			self.root.config(menu=menubar)
			self.root.mainloop()

	def Opzioni(self):
		filename = ""
		def Path():
			nonlocal filename
			filename = filedialog.askdirectory()
			opzioni.lift()
			opzioni.attributes("-topmost", True)
			path_attuale["text"] = filename
		def Salva():
			default = default_c.get()
			file = open("opzioni.json","r", encoding="utf-8")
			preferenze = json.loads(file.read())
			file.close()
			preferenze["default"] = default
			if filename != "":
				preferenze["path"] = filename+"/"
			file = open("opzioni.json","w", encoding="utf-8")
			file.write(json.dumps(preferenze))
			file.close()
			opzioni.destroy()
		file = open("opzioni.json","r", encoding="utf-8")
		preferenze = json.loads(file.read())
		file.close()
		opzioni = tk.Tk()
		opzioni.title("Opzioni")
		opzioni.geometry("400x250")
		default_l = ttk.Label(opzioni, text="Modulo di apertura:", padding = [0,10,0,10], font = 'Arial 10')
		default_c = ttk.Combobox(opzioni, state = 'readonly')
		default_c['values'] = json.loads(open("moduli.json").read())
		default_c.current(default_c["values"].index(preferenze["default"]))
		empty_l = ttk.Label(opzioni, padding = [0,20,0,20])
		path_l = ttk.Label(opzioni, text="Cartella di destinazione:", padding = [0,10,0,10], font = 'Arial 10')
		if preferenze["path"] == "":
			path_attuale = ttk.Label(opzioni, text="Stessa cartella del programma", padding = [0,0,0,10], font = 'Arial 10')
		else:
			path_attuale = ttk.Label(opzioni, text=preferenze["path"], padding = [0,0,0,10], font = 'Arial 10')
		path_b = ttk.Button(opzioni, text="Sfoglia...", command = Path)
		default_l.pack()
		default_c.pack()
		path_l.pack()
		path_attuale.pack()
		path_b.pack()
		empty_l.pack()
		button = ttk.Button(opzioni, text="Salva", command = Salva)
		button.pack()

	def ExtractAnnunci(self,indirizzo,funzione,next,referer):
		t = tk.Toplevel(self.root)
		t.geometry("300x80")
		ttk.Label(t,text="Sto caricando gli annunci, attendere prego",padding = [0,10,0,10]).pack()
		self.bar = ttk.Progressbar(t,mode = 'indeterminate', length = "250")
		self.bar.pack()
		self.bar.start()
		if not referer:
			req = request.Request(indirizzo,headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36', "referer": "https://www.idealista.it/", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "accept-language": "it,en;q=0.9,en-US;q=0.8", "cache-control": "no-cache", "cookie": "pxvid=74ce6d80-3c17-11e8-815a-adb8acaa87c9; _pxvid=74ce6d80-3c17-11e8-815a-adb8acaa87c9; userUUID=48496526-372d-4ddc-b99a-d880ec2ea91d; xtvrn=$402916$; xtan402916=2-anonymous; xtant402916=1; cookieDirectiveClosed=true; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582070-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; optimizelyEndUserId=oeu1523293211328r0.6761614747531912; SESSION=bb1de1c1-42d0-49a6-be91-d3c3e10c57c0; WID=462e24673e309bda|Wsucc|Wsucc; utag_main=v_id:0162ab59ca02000b43bc6b293a1b02087001907f0086e$_sn:1$_ss:0$_st:1523295112843$ses_id:1523293211139%3Bexp-session$_pn:2%3Bexp-session; _px2=eyJ1IjoiYjM4ZTFlMzAtM2MxNy0xMWU4LTgwZDctNmJlOGIyMjg0M2Y5IiwidiI6Ijc0Y2U2ZDgwLTNjMTctMTFlOC04MTVhLWFkYjhhY2FhODdjOSIsInQiOjE1MjMyOTM2MTMwOTcsImgiOiI3NGExNTkwODcwZjQ2YzkxMjQ3NTM5NWQ1MmExNGIyYTM4ZGYyNmMwNmNlY2JlZDRjYTZjYWJlYjE4NGFhOTkxIn0=", "pragma": "no-cache", "upgrade-insecure-requests": "1"})
		else:
			req = request.Request(indirizzo,headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36', "referer": "https://www.idealista.it/", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "accept-language": "it,en;q=0.9,en-US;q=0.8", "cache-control": "no-cache", "cookie": "pxvid=74ce6d80-3c17-11e8-815a-adb8acaa87c9; _pxvid=74ce6d80-3c17-11e8-815a-adb8acaa87c9; userUUID=48496526-372d-4ddc-b99a-d880ec2ea91d; xtvrn=$402916$; xtan402916=2-anonymous; xtant402916=1; cookieDirectiveClosed=true; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582070-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; optimizelyEndUserId=oeu1523293211328r0.6761614747531912; SESSION=bb1de1c1-42d0-49a6-be91-d3c3e10c57c0; WID=462e24673e309bda|Wsucc|Wsucc; utag_main=v_id:0162ab59ca02000b43bc6b293a1b02087001907f0086e$_sn:1$_ss:0$_st:1523295112843$ses_id:1523293211139%3Bexp-session$_pn:2%3Bexp-session; _px2=eyJ1IjoiYjM4ZTFlMzAtM2MxNy0xMWU4LTgwZDctNmJlOGIyMjg0M2Y5IiwidiI6Ijc0Y2U2ZDgwLTNjMTctMTFlOC04MTVhLWFkYjhhY2FhODdjOSIsInQiOjE1MjMyOTM2MTMwOTcsImgiOiI3NGExNTkwODcwZjQ2YzkxMjQ3NTM5NWQ1MmExNGIyYTM4ZGYyNmMwNmNlY2JlZDRjYTZjYWJlYjE4NGFhOTkxIn0=", "pragma": "no-cache", "upgrade-insecure-requests": "1"})
		pagina_vergine = request.urlopen(req).read()
		pagina = pq(pagina_vergine)
		lista = funzione(pagina)
		while next(pagina,indirizzo) != False:
			indirizzo_n = next(pagina,indirizzo)
			print("Indirizzo: "+indirizzo+"\n indirizzo_n_ "+indirizzo_n)
			req = request.Request(indirizzo_n,headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36', "referer": "https://www.idealista.it/", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "accept-language": "it,en;q=0.9,en-US;q=0.8", "cache-control": "no-cache", "cookie": "pxvid=74ce6d80-3c17-11e8-815a-adb8acaa87c9; _pxvid=74ce6d80-3c17-11e8-815a-adb8acaa87c9; userUUID=48496526-372d-4ddc-b99a-d880ec2ea91d; xtvrn=$402916$; xtan402916=2-anonymous; xtant402916=1; cookieDirectiveClosed=true; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582070-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; optimizelyEndUserId=oeu1523293211328r0.6761614747531912; SESSION=bb1de1c1-42d0-49a6-be91-d3c3e10c57c0; WID=462e24673e309bda|Wsucc|Wsucc; utag_main=v_id:0162ab59ca02000b43bc6b293a1b02087001907f0086e$_sn:1$_ss:0$_st:1523295112843$ses_id:1523293211139%3Bexp-session$_pn:2%3Bexp-session; _px2=eyJ1IjoiYjM4ZTFlMzAtM2MxNy0xMWU4LTgwZDctNmJlOGIyMjg0M2Y5IiwidiI6Ijc0Y2U2ZDgwLTNjMTctMTFlOC04MTVhLWFkYjhhY2FhODdjOSIsInQiOjE1MjMyOTM2MTMwOTcsImgiOiI3NGExNTkwODcwZjQ2YzkxMjQ3NTM5NWQ1MmExNGIyYTM4ZGYyNmMwNmNlY2JlZDRjYTZjYWJlYjE4NGFhOTkxIn0=", "pragma": "no-cache", "upgrade-insecure-requests": "1"})
			pagina_vergine = request.urlopen(req).read()
			pagina = pq(pagina_vergine)
			lista += funzione(pagina)
			indirizzo = indirizzo_n
		lista += funzione(pagina)
		t.destroy()
		return lista

	def ExtractData(self,indirizzo,nome_doc,funzioni, referer):
		if not referer:
			req = request.Request(indirizzo,headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36', "referer": "https://www.idealista.it/", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "accept-language": "it,en;q=0.9,en-US;q=0.8", "cache-control": "no-cache", "cookie": "pxvid=74ce6d80-3c17-11e8-815a-adb8acaa87c9; _pxvid=74ce6d80-3c17-11e8-815a-adb8acaa87c9; userUUID=48496526-372d-4ddc-b99a-d880ec2ea91d; xtvrn=$402916$; xtan402916=2-anonymous; xtant402916=1; cookieDirectiveClosed=true; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582070-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; optimizelyEndUserId=oeu1523293211328r0.6761614747531912; SESSION=bb1de1c1-42d0-49a6-be91-d3c3e10c57c0; WID=462e24673e309bda|Wsucc|Wsucc; utag_main=v_id:0162ab59ca02000b43bc6b293a1b02087001907f0086e$_sn:1$_ss:0$_st:1523295112843$ses_id:1523293211139%3Bexp-session$_pn:2%3Bexp-session; _px2=eyJ1IjoiYjM4ZTFlMzAtM2MxNy0xMWU4LTgwZDctNmJlOGIyMjg0M2Y5IiwidiI6Ijc0Y2U2ZDgwLTNjMTctMTFlOC04MTVhLWFkYjhhY2FhODdjOSIsInQiOjE1MjMyOTM2MTMwOTcsImgiOiI3NGExNTkwODcwZjQ2YzkxMjQ3NTM5NWQ1MmExNGIyYTM4ZGYyNmMwNmNlY2JlZDRjYTZjYWJlYjE4NGFhOTkxIn0=", "pragma": "no-cache", "upgrade-insecure-requests": "1"})
		else:
			req = request.Request(indirizzo,headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36', "referer": "https://www.idealista.it/", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "accept-language": "it,en;q=0.9,en-US;q=0.8", "cache-control": "no-cache", "cookie": "pxvid=74ce6d80-3c17-11e8-815a-adb8acaa87c9; _pxvid=74ce6d80-3c17-11e8-815a-adb8acaa87c9; userUUID=48496526-372d-4ddc-b99a-d880ec2ea91d; xtvrn=$402916$; xtan402916=2-anonymous; xtant402916=1; cookieDirectiveClosed=true; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582070-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; optimizelyEndUserId=oeu1523293211328r0.6761614747531912; SESSION=bb1de1c1-42d0-49a6-be91-d3c3e10c57c0; WID=462e24673e309bda|Wsucc|Wsucc; utag_main=v_id:0162ab59ca02000b43bc6b293a1b02087001907f0086e$_sn:1$_ss:0$_st:1523295112843$ses_id:1523293211139%3Bexp-session$_pn:2%3Bexp-session; _px2=eyJ1IjoiYjM4ZTFlMzAtM2MxNy0xMWU4LTgwZDctNmJlOGIyMjg0M2Y5IiwidiI6Ijc0Y2U2ZDgwLTNjMTctMTFlOC04MTVhLWFkYjhhY2FhODdjOSIsInQiOjE1MjMyOTM2MTMwOTcsImgiOiI3NGExNTkwODcwZjQ2YzkxMjQ3NTM5NWQ1MmExNGIyYTM4ZGYyNmMwNmNlY2JlZDRjYTZjYWJlYjE4NGFhOTkxIn0=", "pragma": "no-cache", "upgrade-insecure-requests": "1"})
		pagina_vergine = request.urlopen(req).read()
		pagina = pq(pagina_vergine)
		dati = ""
		for i in range(len(funzioni)):
			dato = funzioni[i](pagina)
			if(i == 0):
				dati = dato
			else:
				dati += "|" + dato
		dati += "|" + indirizzo
		file = open(nome_doc,"a")
		file.write(dati+"\n")
		file.close()
