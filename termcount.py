#!/usr/local/bin/python3.5
# -*-coding:Utf-8 -*
import codecs
import re
from html.parser import HTMLParser
from collections import Counter
from pickle import Pickler

import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize


#parser = CountingParser(stopwords)
# reuterfnames = [
# 	'data/reut2-000.sgm',
# 	'data/reut2-001.sgm',
# 	'data/reut2-002.sgm',
# 	'data/reut2-003.sgm',
# 	'data/reut2-004.sgm',
# 	'data/reut2-005.sgm',
# 	'data/reut2-006.sgm',
# 	'data/reut2-007.sgm',
# 	'data/reut2-008.sgm',
# 	'data/reut2-009.sgm',
# 	'data/reut2-010.sgm',
# 	'data/reut2-011.sgm',
# 	'data/reut2-012.sgm',
# 	'data/reut2-013.sgm',
# 	'data/reut2-014.sgm',
# 	'data/reut2-015.sgm',
# 	'data/reut2-016.sgm',
# 	'data/reut2-017.sgm',
# 	'data/reut2-018.sgm',
# 	'data/reut2-019.sgm',
# 	'data/reut2-020.sgm',
# 	'data/reut2-021.sgm']
#for fname in reuterfnames :
#	reuterfile = open(fname, 'r')
#	parser.feed(reuterfile.read())
#	reuterfile.close()

#with open('reuter_parsed','wb') as reuterp :
#	Pickler(reuterp).dump(parser.doclist)

def parse_document(str, stopwords=None):
    """
    :param str: the string to tokenize and put in a dict
    :return: the dictionnary with the number of occurences in each word, the number of different words and the total number of occurences
    """

    if stopwords is None:
        stopwords = {}

    data = word_tokenize(str)
    d = {}
    for word in data:
        if word in stopwords:
            continue

        if word in d:
            d[word]+=1
        else:
            d[word]=1

    s = 0
    for entry in d.values():
        s += entry

    return d, len(d), s

def parse_reuters(filename, stopwords):
    return [parse_document(x.getText(), stopwords) for x in BeautifulSoup(codecs.open(filename, 'r', 'utf-8').read(), "html.parser").find_all(
        'reuters')]

if __name__ == "__main__":
    with open('data/stopwords') as stwordfile:
        stopwords = stwordfile.read().split()
    reuterfnames = [
        'data/reut2-000.sgm',
        'data/reut2-001.sgm',
        'data/reut2-002.sgm',
        'data/reut2-003.sgm',
        'data/reut2-004.sgm',
        'data/reut2-005.sgm',
        'data/reut2-006.sgm',
        'data/reut2-007.sgm',
        'data/reut2-008.sgm',
        'data/reut2-009.sgm',
        'data/reut2-010.sgm',
        'data/reut2-011.sgm',
        'data/reut2-012.sgm',
        'data/reut2-013.sgm',
        'data/reut2-014.sgm',
        'data/reut2-015.sgm',
        'data/reut2-016.sgm',
    #	'data/reut2-017.sgm',
        'data/reut2-018.sgm',
        'data/reut2-019.sgm',
        'data/reut2-020.sgm',
        'data/reut2-021.sgm']
    documents = []
    for fname in reuterfnames:
        documents += parse_reuters(fname, stopwords)

    print(documents[0])
    print(len(documents))

    with open('reuter_parsed', 'wb') as reuterp:
        Pickler(reuterp).dump(documents)