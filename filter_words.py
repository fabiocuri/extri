#!/usr/bin/env python
# coding: utf-8

''' 
Author: Fabio Curi Paixao 
fcuri91@gmail.com
 '''

from export_abstracts import read_as_list, write_list
from os import listdir

if '__main__' == __name__:

    ''' Removes wrong genes '''

    to_avoid = read_as_list('to_avoid.txt', encoding='latin-1')
    l_ann = [f for f in listdir('./test/merged/') if f.endswith('.minfner')]

    for a in l_ann:

        ann = read_as_list('./test/merged/' + a, encoding='latin-1')
        final = []
        for p in ann:
           if p.split('\t')[2] not in to_avoid:
               final.append(p)    

        write_list(list(set(final)), './test/merged/' + a + '.ann', True, 'latin-1')


