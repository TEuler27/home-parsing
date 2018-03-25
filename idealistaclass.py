def BuildLink(ven_aff,provincia,comune,zona):
	if ven_aff == "":
		a = messagebox.showerror("Errore", "Alcuni dati sono mancanti")
		return False
	if provincia == "":
		messagebox.showerror("Errore", "Alcuni dati sono mancanti")
		return False
	link = "https://www.idealista.it/"
	if ven_aff == "Vendita":
		link += "vendita-case/"
	else:
		link += "affitto-case/"
	if comune != "" and zona == "":
		return link+comune.lower().replace(" ", "-")+"-"+provincia.lower().replace(" ","-")+"/"
	if zona != "":
		return link+comune.lower().replace(" ", "-")+"/"+zona.lower().replace(" ","-")+"/"
	if "-" in provincia:
		return link+provincia.lower().replace(" ","-")+"/"
	else:
		return link+provincia.lower().replace(" ","-")+"-provincia/"
