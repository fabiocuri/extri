#!/usr/bin/env python
# coding: utf-8

''' 
Author: Fabio Curi Paixao
E-mail: fcuri91@gmail.com
Date: 07.10.2019
'''

import os
import re
import argparse

def read_as_list(l, encoding):

    ''' Reads file as list. '''

    l_ = []
    with open(l, "rt", encoding=encoding) as f:
        l_ = f.read().splitlines()
    return l_

def write_list(l, l_name, iterate, encoding):

    ''' Exports list. '''

    with open(l_name, 'w', encoding=encoding) as f:
        if iterate:
            for item in l:
                f.write("%s\n" % item)
        else:
            f.write("%s\n" % l)

if '__main__' == __name__:

    ''' Exports pubtator abstracts as .txt files. '''

    encoding = 'latin-1'

    parser = argparse.ArgumentParser(description='Options')
    parser.add_argument('--i', type=str, help="""Input directory.""")
    parser.add_argument('--o', type=str, help="""Output directory.""")
    args = parser.parse_args()

    in_folder = args.i
    out_folder = args.o
    articles = [f for f in os.listdir(in_folder) if f.endswith('.txt')]

    for PMID in articles:
        article = read_as_list(in_folder + '/' + PMID, encoding=encoding)
        try:
            article = article[-2].split('|')[2]
            article = re.sub(r'[^\x00-\x7f]', r' ', article)  # ASCII
            write_list(article, out_folder + '/' + PMID, iterate=False, encoding=encoding)
        except:
            continue
