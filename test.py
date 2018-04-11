from pyquery import PyQuery as pq
from urllib import request

for n in range(200):
	req = request.Request("https://www.idealista.it/immobile/12210206/",headers={"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",

"accept-language": "it,en;q=0.9,en-US;q=0.8",
"cache-control": "no-cache",
"cookie": "userUUID=47d964f2-c471-48e4-9d1d-e3e9828ac51a; xtvrn=$402916$; xtan402916=2-anonymous; xtant402916=1; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582070-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; cookieDirectiveClosed=true; pxvid=ffb6a610-3c3a-11e8-b188-fdebed1960a3; optimizelyEndUserId=oeu1523308473192r0.013028662740697916; _pxvid=ffb6a610-3c3a-11e8-b188-fdebed1960a3; SESSION=863e55c2-41dc-458c-80be-c226fbd57e90; WID=642ac56477c49ed0|Ws4rQ|Ws4lN; utag_main=v_id:0162ac42a9dd00917237be61127802087001907f0086e$_sn:2$_ss:0$_st:1523462749490$ses_id:1523458452272%3Bexp-session$_pn:8%3Bexp-session; _px2=eyJ1IjoiY2QwMDQ2YTAtM2Q5Yy0xMWU4LWFjODktNmRhNDYxYmNmNWZjIiwidiI6ImZmYjZhNjEwLTNjM2EtMTFlOC1iMTg4LWZkZWJlZDE5NjBhMyIsInQiOjE1MjM0NjI0MTYyNjIsImgiOiJjNTZmYzZiYjQ4MzA1NmI1M2QxZGM2MzJmMWU4MmM5YmI3YzZlYmQ4YjljNjgxMjhhNjBkNWM1NGQwYzMwNzFmIn0=",
"pragma": "no-cache",
"upgrade-insecure-requests": "1",
"referer": "https://www.idealista.it",
"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"})
	pagina = request.urlopen(req).read()
	print(pagina[:10])
