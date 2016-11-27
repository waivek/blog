
from bs4 import BeautifulSoup
import sys
import io


permalink='<a href="#para%d">permalink</a>'

html=open("final.html", encoding="utf-8").read()

soup=BeautifulSoup(html, "lxml")

for i, p in enumerate(soup.select("div.c1 > p")):
    lnk = permalink % (i+1)
    new_a = BeautifulSoup(lnk, "lxml").a
    p['id']="para%d" % (i+1)
    p.append(new_a)

with open("test.html", "wb") as f:
    f.write(soup.prettify("utf-8"))

print("Done")
