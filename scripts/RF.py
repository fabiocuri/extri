#!/usr/bin/env python
# coding: utf-8

''' 
Author: Fabio Curi Paixao
E-mail: fcuri91@gmail.com
Date: 07.10.2019
'''

import os
import nltk
import scipy
import argparse
import numpy as np
from scipy.sparse import hstack
from collections import defaultdict
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from export_abstracts import read_as_list, write_list
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import f1_score, precision_score, recall_score

def run_RF(X, test_x, labels_x, f, REPORT, out_dir, dic_dir):

    np.random.seed(500)

    if REPORT == 'yes':
        n_folds = 1
    if REPORT == 'no':
        n_folds = 10

    VALIDATION_SPLIT = 0.2 # Validation %
    l_precision, l_recall, l_f1 = [], [], []

    for n_ in range(n_folds):

        print('Running fold ' + str(n_))

        Encoder = LabelEncoder()
        labels = Encoder.fit_transform(labels_x)

        if f == 'TF-IDF':
            vect = TfidfVectorizer(max_features=1000)
        if f == 'BoW':
            vect = CountVectorizer(max_features=1000)

        vect.fit(X)
        Train_X_Tfidf = vect.transform(X)
        features_train = build_features(dic_dir, X)
        train = hstack((Train_X_Tfidf, features_train))

        if REPORT == 'yes':
            Test_X_Tfidf = vect.transform(test_x)
            features_test = build_features(dic_dir, test_x)
            test = hstack((Test_X_Tfidf, features_test))

        RF = RandomForestClassifier(random_state=0, n_estimators=100)

        if not os.path.exists(out_dir + '/models'):
            os.makedirs(out_dir + '/models')

        if REPORT == 'yes':
            RF.fit(train,labels)
            y_pred = RF.predict(test)
            write_list(y_pred, out_dir + '/models/re_predictions.txt', iterate=True, encoding=encoding)

        if REPORT == 'no':
            train, test, labels, test_labels = train_test_split(train, labels, test_size=VALIDATION_SPLIT, random_state=42)
            RF.fit(train,labels)
            y_pred = RF.predict(test)

            l_precision.append(precision_score(y_true=test_labels, y_pred=y_pred, average='macro'))
            l_recall.append(recall_score(y_true=test_labels, y_pred=y_pred, average='macro'))
            l_f1.append(f1_score(y_true=test_labels, y_pred=y_pred, average='macro'))

    if REPORT == 'no':

        l_results = 're_RF' + '\t' + str(np.mean(l_precision)) + '\t' + str(np.mean(l_recall)) + '\t' + str(np.mean(l_f1))
        print(l_results)

def build_features(dic_dir, documents):

    list_words = read_as_list(dic_dir + '/dictionary_features.txt', encoding='latin-1')
    final = []
   
    for d in documents:
        export = []
        c = defaultdict(lambda: 0)
        for w in nltk.word_tokenize(d):
            c[str(w)] = +1
        for w in list_words:
            if c[str(w)] > 0:
                export += [1]
            else:
                export += [0]

        final.append(export)

    return scipy.sparse.csr_matrix(final)

if '__main__' == __name__:

    ''' Run Random Forest '''

    encoding = 'latin-1'
    cwd = os.getcwd()

    parser = argparse.ArgumentParser(description='Hyper-parameters of the model.')
    parser.add_argument('--train', type=str, help="""Train file.""")
    parser.add_argument('--test', type=str, help="""Test file.""")
    parser.add_argument('--labels', type=str, help="""Labels file.""")
    parser.add_argument('--features', type=str, help="""Features to be used.""")
    parser.add_argument('--report', type=str, help="""If yes, predict unseen data.""")
    parser.add_argument('--dictionary', type=str, help="""Dictionary directory.""")
    parser.add_argument('--o', type=str, help="""Output folder.""")
    args = parser.parse_args()

    train = read_as_list(args.train, encoding='latin-1')
    if args.report == 'yes':
        test = read_as_list(args.test, encoding='latin-1')
    if args.report == 'no':
        test = []
    labels = read_as_list(args.labels, encoding='latin-1')

    f = args.features
    REPORT = args.report
    out_dic = args.o
    dic_dir = args.dictionary

    run_RF(train, test, labels, f, REPORT, out_dic, dic_dir)
