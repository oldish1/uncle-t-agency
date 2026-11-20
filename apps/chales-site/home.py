import re, json, sys, os, glob
os.chdir(sys.argv[1]); B="https://chaleshairboutique.co.za"
for p in ["index.html"]+glob.glob("*/index.html"):
    s=open(p,encoding="utf-8").read()
    s=s.replace("Chanté blow-drying a burgundy colour","Stylist blow-drying a burgundy colour")
    open(p,"w",encoding="utf-8").write(s)
s=open("index.html",encoding="utf-8").read()
# 1. one canonical, consistent og:url
s=s.replace(f'  <link rel="canonical" href="{B}" />\n','',1)
s=s.replace(f'<meta property="og:url" content="{B}" />',f'<meta property="og:url" content="{B}/" />')
assert s.count('rel="canonical"')==1
# 2. H1 that says what the business is, same look
s=s.replace('<h1 class="hero-title">CHALES</h1>','<h1 class="hero-title">CHALES<span class="sr-only"> Hair Boutique, hair salon in Bellville, Cape Town</span></h1>')
s=s.replace('</style>','    .sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }\n  </style>',1)
# 3. structured data: same salon record as the service pages + FAQ + website
sub=open("nanoplastia/index.html",encoding="utf-8").read()
salon=[n for n in json.loads(re.search(r'ld\+json">(.*?)</script>',sub,re.S).group(1))["@graph"] if n["@type"]=="HairSalon"][0]
salon["image"]=f"{B}/chales-hair-boutique-bellville.jpg"
salon["description"]="Luxury hair salon in Oakdale, Bellville, Cape Town. Hair colour, highlights, balayage, keratin, Brazilian blowouts, Nanoplastia, hair botox and precision cuts. Book with Lexi on WhatsApp."
salon["founder"]={"@type":"Person","name":"Chanté"}
salon["paymentAccepted"]="Cash, Card, EFT"; salon["currenciesAccepted"]="ZAR"
salon["hasOfferCatalog"]={"@type":"OfferCatalog","name":"Hair services and prices","url":f"{B}/prices/"}
salon["potentialAction"]={"@type":"ReserveAction","target":"https://wa.me/27714296057"}
faq=[]
for q,a in re.findall(r'faq-question-text">(.*?)</span>.*?faq-answer-inner">(.*?)</div>',s,re.S):
    faq.append({"@type":"Question","name":q.strip(),"acceptedAnswer":{"@type":"Answer","text":re.sub("<[^>]+>","",a).strip()}})
graph={"@context":"https://schema.org","@graph":[salon,
  {"@type":"WebSite","@id":f"{B}/#website","url":f"{B}/","name":"CHALES Hair Boutique","publisher":{"@id":salon["@id"]},"inLanguage":"en-ZA"},
  {"@type":"FAQPage","mainEntity":faq}]}
s,n=re.subn(r'(<script type="application/ld\+json">).*?(</script>)',lambda m:m.group(1)+"\n"+json.dumps(graph,ensure_ascii=False,indent=2)+"\n  "+m.group(2),s,count=1,flags=re.S)
assert n==1
# 4. link the full price page from the homepage price list
anchor='<span class="price-amount"><a href="tel:+27814332756" style="color:var(--gold); text-decoration:none;">081 433 2756</a></span>\n      </div>'
assert anchor in s
s=s.replace(anchor,anchor+'\n      <p style="text-align:center; margin-top:2rem;"><a href="/prices/" style="color:var(--gold); letter-spacing:.08em;">See the full CHALES price list &rarr;</a></p>',1)
# geo + language hints like the service pages
s=s.replace('<meta charset="UTF-8" />','<meta charset="UTF-8" />\n  <meta name="geo.region" content="ZA-WC" />\n  <meta name="geo.placename" content="Bellville, Cape Town" />',1)
open("index.html","w",encoding="utf-8").write(s)
print("faq items",len(faq)); print(re.search(r'<html[^>]*>',s).group(0))
