import json,urllib.parse,urllib.request,time,os,re,sys
API="https://es.wikisource.org/w/api.php"
UA="SpanishStoryCollector/1.0 (https://github.com/alejandroechev public-domain anthology)"
def parse(title):
    p={"action":"parse","page":title,"prop":"text|wikitext","format":"json","formatversion":"2"}
    r=urllib.request.Request(API+"?"+urllib.parse.urlencode(p),headers={"User-Agent":UA})
    time.sleep(3); return json.load(urllib.request.urlopen(r))
titles=sys.argv[1:]
for t in titles:
    try: d=parse(t)
    except Exception as e: print("ERR",t,e); continue
    if "error" in d: print("ERR",t,d["error"]); continue
    html=d["parse"]["text"]; wt=d["parse"]["wikitext"]
    fn="raw/"+re.sub(r'[^A-Za-z0-9]+','_',t)+".json"
    json.dump({"title":t,"html":html,"wikitext":wt},open(fn,"w"),ensure_ascii=False)
    text=re.sub(r'<[^>]+>',' ',html); text=re.sub(r'\s+',' ',text)
    print(f"{len(text.split()):>7} words  {t}  -> {fn}")
    print("   WT head:",wt[:260].replace("\n"," | "))
