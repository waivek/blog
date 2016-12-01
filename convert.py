"""Website Converter

Usage:
  convert.py [options] <input_regex>...
  convert.py (-h | --help)
  convert.py --version

Options:
  -h --help              Show this screen.
  --version              Show version.
  --output=FILE -o FILE  Output File
"""
# python conver.py **/*.md raws

import pypandoc
from bs4 import BeautifulSoup
import sys
from os.path import basename, splitext, dirname, join, isfile, abspath
from os import listdir
import argparse
from docopt import docopt
import glob

def get_file_name_and_ext(path):
    base=basename(path) #base=c.txt
    name,ext=splitext(base) #name,ext=('c', '.txt')
    return name,ext


def get_file_name(path): # path=a/b/c.txt
    name,ext=get_file_name_and_ext(path)
    return name

def add_permalink_to_paras(soup):
    for i, p in enumerate(soup.select("div.c1 > p"), start=1):
        p['id'] = "para%d" % i
        lnk = '<a href="#%s">§</a>' % p['id']
        new_a = BeautifulSoup(lnk, "lxml").a
        # p.append(new_a)
        p.insert(0, new_a)

    return soup

def markdown_to_html(md_file):
    # TEMPLATE_FILE=r"C:\Users\Toshiba PC\Desktop\static\template.html"
    # TEMPLATE_FILE="template.html"
    # __file__ = ..\convert.py
    dir=dirname(__file__) # dir = ..
    TEMPLATE_FILE=join(dir, "template.html") # template=..\template.html

    html = pypandoc.convert(
        md_file,
        format="markdown",
        to="html",
        # extra_args=["--template="+TEMPLATE_FILE.strip()]
        extra_args=["--template="]
    )
    soup=BeautifulSoup(html, "lxml")
    soup=add_permalink_to_paras(soup)
    return soup.prettify("utf-8")

def write_html(file_name, html):
    with open(file_name, "wb") as f:
        f.write(html)

def convert_markdown_file_to_html_file(markdown_file, html_file):
    write_html(html_file, markdown_to_html(markdown_file))

def is_markdown_file(file):
    _, ext= get_file_name_and_ext(file)
    # print(ext)
    return ext == ".md" and isfile(file)

def get_markdown_files(dir="."):
    # print(listdir(dir))
    lst= [f for f in listdir(dir) if is_markdown_file(join(dir, f))]
    return lst

def change_ext_to(file, new_ext):
    return get_file_name(file) + "." + new_ext

def convert_md_in_directory(input_dir=".", output_dir="."):
    for md_file in get_markdown_files(input_dir):
        html_file = join(output_dir, change_ext_to(md_file, "html"))
        convert_markdown_file_to_html_file(md_file, html_file)
        print("%s -> %s" % (md_file, html_file))


def main():
    arguments = docopt(__doc__, version='Website generator 1.0')
    inputs=arguments["<input_regex>"]
    input_files = []
    for input in inputs:
        input_files = input_files + glob.glob(input)

    dir = arguments["--output"] or "."

    for input_file in input_files:
        output_file = join(dir, change_ext_to( input_file,"html"))
        convert_markdown_file_to_html_file(input_file, output_file)





if __name__ == '__main__':
    main()


print("Done")
