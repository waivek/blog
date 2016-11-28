import pypandoc
from bs4 import BeautifulSoup
import sys
from os.path import basename, splitext, dirname, join

def get_file_name(path): # path=a/b/c.txt
    base=basename(path) #base=c.txt
    name,ext=splitext(base) #name,ext=('c', '.txt')
    return name

def add_permalink_to_paras(soup):
    for i, p in enumerate(soup.select("div.c1 > p"), start=1):
        p['id'] = "para%d" % i
        lnk = '<a href="#%s">permalink</a>' % p['id']
        new_a = BeautifulSoup(lnk, "lxml").a
        p.append(new_a)
    return soup

def markdown_to_html(md_file):
    # __file__ = ..\convert.py
    dir=dirname(__file__) # dir = ..
    template=join(dir, "template.html") # template=..\template.html
    print(template)

    html = pypandoc.convert(
        md_file,
        format="markdown",
        to="html",
        extra_args=["--template="+template]
    )
    soup=BeautifulSoup(html, "lxml")
    soup=add_permalink_to_paras(soup)
    return soup.prettify("utf-8")

def write_html(file_name, html):
    with open(file_name, "wb") as f:
        f.write(html)

def convert_markdown_file_to_html_file(markdown_file, html_file):
    write_html(html_file, markdown_to_html(markdown_file))

def main():
    if len(sys.argv) == 1:
        print("Enter a file name")
        return
    input_file = sys.argv[1] # input_file=1.md

    output_file = None
    if len(sys.argv) == 2:
        output_file = get_file_name(input_file) + ".html" # output_file=1.html
    else:
        output_file = sys.argv[2]

    convert_markdown_file_to_html_file(input_file, output_file)

if __name__ == "__main__":
    main()


