"""Website Converter

Usage:
  convert.py <input_file> [<output_file>]
  convert.py --all [<input_directory>] [<output_directory>]
  convert.py (-h | --help)
  convert.py --version

Options:
  -h --help                Show this screen.
  --version                Show version.
  --all                    Transform entire directory in-place
"""

import pypandoc
from bs4 import BeautifulSoup
import sys
from os.path import basename, splitext, dirname, join, isfile
from os import listdir
import argparse
from docopt import docopt

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
    # __file__ = ..\convert.py
    dir=dirname(__file__) # dir = ..
    template=join(dir, "template.html") # template=..\template.html

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

def convert_md_in_directory(dir="."):
    for md_file in get_markdown_files(dir):
        html_file = change_ext_to(md_file, "html")
        convert_markdown_file_to_html_file(md_file, html_file)
        print("%s -> %s" % (md_file, html_file))


def main():
    # if len(sys.argv) == 1: # python converty.py <CR>
    #     print("Enter a file name")
    #     return
    # input_file = sys.argv[1] # input_file=1.md
    #
    # output_file = None
    # if len(sys.argv) == 2: # python convert.py input.md <CR>
    #     output_file = change_ext_to(input_file, "html") # output_file=1.html
    # else: # python convert.py input.md output.html <CR>
    #     output_file = sys.argv[2]
    #
    # convert_markdown_file_to_html_file(input_file, output_file)

    arguments = docopt(__doc__, version='Website generator 1.0')
    if not arguments["--all"]:
        input_file = arguments['<input_file>']
        output_file = arguments['<output_file>']
        if not output_file:
            output_file = change_ext_to(input_file, "html") # output_file=1.html
        convert_markdown_file_to_html_file(input_file, output_file)
    else:
        input_dir = arguments["<input_directory>"]

        convert_md_in_directory(input_dir)




if __name__ == '__main__':
    main()


print("Done")
