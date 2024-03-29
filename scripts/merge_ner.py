#!/usr/bin/env python
# coding: utf-8

''' 
Author: Fabio Curi Paixao
E-mail: fcuri91@gmail.com
Date: 07.10.2019
'''

import os
import argparse
from os import listdir
from export_abstracts import read_as_list, write_list

cwd = os.getcwd()

def merge(f, f2, f3, f_out):

    l_ntnu = [f for f in listdir(f) if f.endswith('.minfner')]
    l_gnormplus = [f for f in listdir(f2) if f.endswith('.minfner')]
    l_text = [f for f in listdir(f3) if f.endswith('.txt')]

    for text in l_text:

        rl, write_out, already, final_merge = [], [], [], []

        tx = read_as_list(f3 + '/' + text, encoding=encoding)
        ann = text + '.out.minfner'
        ntnu_boolean, gn_boolean = False, False

        if ann in l_ntnu:
            ntnu = read_as_list(f + '/' + ann, encoding=encoding)
            ntnu = ['N_' + s  for s in ntnu]
            ntnu_boolean = True

        ann = text.split('.')[0] + ':0.txt.out.minfner'
        if ann in l_gnormplus:
            gn = read_as_list(f2 + '/' + ann, encoding=encoding)
            gn = ['G_' + s  for s in gn]
            gn_boolean = True

        # Merge both tools and keep only entities
        if ntnu_boolean and gn_boolean:
            entities = ntnu + gn
        elif ntnu_boolean and not gn_boolean:
            entities = ntnu
        elif not ntnu_boolean and gn_boolean:
            entities = gn
        else:
            entities = False

        # Keep all N_DBTF
        final_merge += [x for x in entities if x[0] == 'N' and x.split('\t')[1].split(' ')[0]=='DBTF']
        already = [(x.split('\t')[1].split(' ')[1], x.split('\t')[1].split(' ')[2]) for x in final_merge if x[2] == 'T']
        # Keep all G_NONDBTF 
        final_merge += [x for x in entities if x[0] == 'G' and x.split('\t')[1].split(' ')[0]=='NONDBTF' and (x.split('\t')[1].split(' ')[1], x.split('\t')[1].split(' ')[2]) not in already]
        already = [(x.split('\t')[1].split(' ')[1], x.split('\t')[1].split(' ')[2]) for x in final_merge if x[2] == 'T']
        # Keep all N_NONDBTF
        final_merge += [x for x in entities if x[0] == 'N' and x.split('\t')[1].split(' ')[0]=='NONDBTF' and (x.split('\t')[1].split(' ')[1], x.split('\t')[1].split(' ')[2]) not in already]
        already = [(x.split('\t')[1].split(' ')[1], x.split('\t')[1].split(' ')[2]) for x in final_merge if x[2] == 'T']
        # Keep all G_DBTF
        final_merge += [x for x in entities if x[0] == 'G' and x.split('\t')[1].split(' ')[0]=='DBTF' and (x.split('\t')[1].split(' ')[1], x.split('\t')[1].split(' ')[2]) not in already]
        already = [(x.split('\t')[1].split(' ')[1], x.split('\t')[1].split(' ')[2]) for x in final_merge if x[2] == 'T']

        elements = [x.split('\t')[0][3:] for x in final_merge]
        final_merge += [x for x in entities if x[0:3] == 'N_#' and x.split('\t')[0][3:] in elements]

        entities = [x[2:] for x in final_merge]

        ann_out = text.split('.')[0] + '.ann'

        if entities:
            for e in entities:
                if e[0] == 'T':
                    e_ = e.split('\t')
                    entity, tag, start, end, word = e_[0], e_[1].split(' ')[0], e_[1].split(' ')[1], e_[1].split(' ')[2], e_[2]
                    write_out.append(str(entity) + '\t' + tag + ' ' + str(start) + ' ' + str(end) + '\t' + word)
                if e[0] == '#':
                    e_ = e.split('\t')
                    entity, ID = e_[0], ' '.join(e_[1].split(' ')[1:]) + ' ' + e_[2]
                    write_out.append(str(entity) + '\t' + 'AnnotatorNotes T' + str(entity[1:]) + '\t' + str(ID))

        if write_out:
            write_list(write_out, f_out + '/' + ann_out, iterate=True, encoding=encoding)
            write_list(tx, f_out + '/' + text, iterate=True, encoding=encoding)

if '__main__' == __name__:

    ''' Exports a final NER annotation. '''

    encoding = 'latin-1'

    parser = argparse.ArgumentParser(description='Options')
    parser.add_argument('--i1', type=str, help="""Data folder.""")
    parser.add_argument('--i2', type=str, help="""Data folder.""")
    parser.add_argument('--i3', type=str, help="""Data folder.""")
    parser.add_argument('--o', type=str, help="""Data folder.""")
    args = parser.parse_args()

    merge(args.i1, args.i2, args.i3, args.o)
