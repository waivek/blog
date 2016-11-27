
from markdown import markdown
from bs4 import BeautifulSoup

doc = open("index.md", encoding="utf-8").read()

html=markdown(doc)
soup=BeautifulSoup(html, "lxml")

footnotes = {}
for i, a in enumerate(soup("a")):
    key = "#ref_" + str(i)
    footnotes[key]=a["href"]
    a["href"]=key