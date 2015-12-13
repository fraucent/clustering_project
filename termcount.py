#!/usr/local/bin/python3.5
# -*-coding:Utf-8 -*
import codecs
import os

from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from pickle import Pickler


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

def parse_reuters(filename, stopwords=None):
    return [parse_document(x.getText(), stopwords) for x in BeautifulSoup(codecs.open(filename, 'r', 'utf-8').read(), "html.parser").find_all(
        'reuters')]

def parse_bagofwords(filename, stopwords=None):
    docs = {}
    idx = 0
    for line in codecs.open(filename, 'r', 'utf-8'):
        if idx % 100000 == 0:
            print(idx)
        idx+=1
        data = [int(x) for x in line.split()]
        if len(data) != 3:
            continue
        if data[0] not in docs:
            docs[data[0]] = {}
        docs[data[0]][data[1]] = data[2]
    return list(docs.values())

def parse_all_reuters():
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
    idx = 0
    if not os.path.exists("data_parsed/reuters/"):
        os.mkdir("data_parsed/reuters/")
    for fname in reuterfnames:
        for doc in parse_reuters(fname, stopwords):
            with open('data_parsed/reuters/'+str(idx), 'wb') as f2:
                Pickler(f2).dump(doc)
            idx+=1

if __name__ == "__main__":
    parse_all_reuters()

    #with open('pubmed_parsed', 'wb') as reuterp:
    #    Pickler(reuterp).dump(parse_bagofwords("data/docword.pubmed.txt"))

    # with open('data/stopwords') as stwordfile:
    #     stopwords = stwordfile.read().split()
    # reuterfnames = [
    #     'data/reut2-000.sgm',
    #     'data/reut2-001.sgm',
    #     'data/reut2-002.sgm',
    #     'data/reut2-003.sgm',
    #     'data/reut2-004.sgm',
    #     'data/reut2-005.sgm',
    #     'data/reut2-006.sgm',
    #     'data/reut2-007.sgm',
    #     'data/reut2-008.sgm',
    #     'data/reut2-009.sgm',
    #     'data/reut2-010.sgm',
    #     'data/reut2-011.sgm',
    #     'data/reut2-012.sgm',
    #     'data/reut2-013.sgm',
    #     'data/reut2-014.sgm',
    #     'data/reut2-015.sgm',
    #     'data/reut2-016.sgm',
    # #	'data/reut2-017.sgm',
    #     'data/reut2-018.sgm',
    #     'data/reut2-019.sgm',
    #     'data/reut2-020.sgm',
    #     'data/reut2-021.sgm']
    # documents = []
    # for fname in reuterfnames:
    #     documents += parse_reuters(fname, stopwords)
    #
    # print(documents[0])
    # print(len(documents))
    #
    # with open('reuter_parsed', 'wb') as reuterp:
    #     Pickler(reuterp).dump(documents)