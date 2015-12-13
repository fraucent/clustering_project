#!/usr/bin/python3.2
# coding=utf-8
import codecs
import math

import struct
from collections import Counter

class TFIDF_reader(object):
    def __init__(self, filename):
        self.storage = open(filename, 'rb')

        self.struct_header = struct.Struct("ii")
        self.doc_nb, self.dict_size = self.struct_header.unpack(self.storage.read(self.struct_header.size))

        self.struct_entry = struct.Struct("id" + ("i" * self.dict_size) + ("d" * self.dict_size))
        self.struct_entry_header = struct.Struct("id")

        print("Computing doc locations")

        self.doc_location = {}
        for i in range(0, self.doc_nb):
            pos = self.struct_header.size + i * self.struct_entry.size
            self.storage.seek(pos)
            self.doc_location[self.struct_entry_header.unpack(self.storage.read(self.struct_entry_header.size))[0]] = pos

        print("Done")

    def read_docId(self, docId):
        return self.read(self.doc_location[docId])

    def read_idx(self, idx):
        return self.read(self.struct_header.size + idx * self.struct_entry.size)

    def read(self, pos):
        self.storage.seek(pos)
        return self.struct_entry.unpack(self.storage.read(self.struct_entry.size))

def tfidf_cosine_distance(vector1, vector2):
    size = int((len(vector1)-2)/2)
    pos1 = 0
    pos2 = 0
    curVal = 0.0
    while pos1 != size and pos2 != size:
        if vector1[2+pos1] == -1 or vector2[2+pos2] == -1:
            break

        if vector1[2+pos1] == vector2[2+pos2]:
            curVal += vector1[2+size+pos1]*vector2[2+size+pos2]
            pos1 += 1
            pos2 += 1
        elif vector1[2 + pos1] < vector2[2 + pos2]:
            pos1 += 1
        else:
            pos2 += 1

    return 1.0 - (curVal / (vector1[1]*vector2[1]))

class TFIDF_computation(object):
    def __init__(self):
        self.words_count = {}
        self.words_documents = {}
        self.max_doc_size = 0
        self.doc_nb = 0
        self.storage = None
        self.words_idx = {}

    def add_word_usage(self, word, count):
        """
        add one to the count of the word in the corpus. Must be called ONCE for each word and each document, if the word appears in it.
        :param word: the word in the current document
        :param count: the number of times this word appear in the current document
        :return:
        """
        if word in self.words_count:
            self.words_count[word] += count
            self.words_documents[word] += 1
        else:
            self.words_count[word] = count
            self.words_documents[word] = 1

    def add_doc_size(self, docsize):
        """
        Update the maximum doc size if this document have a greater word number.
        :param docsize:
        """
        self.max_doc_size = max(docsize, self.max_doc_size)
        self.doc_nb += 1

    def init_storage(self, filename, filenameWord):
        """
        Init the storage. Must be call after all the calls to add_word_usage and add_doc_size.
        :param filename:
        :param filenameWord:
        """
        self.storage = open(filename, 'wb')
        self.storage.write(struct.Struct("ii").pack(self.doc_nb, self.max_doc_size))
        self.struct = struct.Struct("id" + ("i" * self.max_doc_size) + ("d" * self.max_doc_size))
        #storageWord = open(filenameWord, 'w')
        #for i, w in enumerate(self.words_count.keys()):
        #    self.words_idx[w] = i
        #    storageWord.write(w+"\t"+str(i)+"\n")
        for i, w in enumerate(self.words_count.keys()):
            self.words_idx[w] = int(w)

    def compute_vector_and_add(self, docid, words):
        """
        Compute the TF-IDF vector for a document and add it to the file
        :param docid: the document id to be stored in the vector
        :param words:
        :return:
        """
        todo = sorted([(self.words_idx[w], w, words[w]) for w in words], key=lambda x:x[0])
        word_count = sum(words.values())

        data = [0.0 for _ in range(0, 2+2*self.max_doc_size)]
        data[0] = docid
        data[1] = 0.0
        for i in range(0, self.max_doc_size):
            if(i >= len(todo)):
                data[2+i] = -1
                data[2+self.max_doc_size+i] = 0
            else:
                idx, word, count = todo[i]
                data[2+i] = idx
                tf = float(count)/float(word_count)
                idf = math.log(float(self.doc_nb)/float(self.words_documents[word]))
                data[2+self.max_doc_size+i] = tf*idf
                data[1] += tf * idf * tf * idf
        data[1] = math.sqrt(data[1])
        f = self.struct.pack(*data)
        self.storage.write(f)

def parse_bagofwords(filename):
    idx = 0
    oldDoc = -1
    currentSize = 0
    tfidfc = TFIDF_computation()

    for line in codecs.open(filename, 'r', 'utf-8'):
        if idx != 0 and idx % 1000000 == 0:
            print(idx)
        idx += 1
        data = [int(x) for x in line.split()]
        if len(data) != 3:
            continue
        if data[0] != oldDoc:
            if currentSize != 0:
                tfidfc.add_doc_size(currentSize)
                currentSize = 0
            oldDoc = data[0]
        tfidfc.add_word_usage(data[1], data[2])
        currentSize+=1
    if currentSize != 0:
        tfidfc.add_doc_size(currentSize)

    tfidfc.init_storage("test.vectors", "")
    idx = 0
    oldDoc = -1
    currentWords = {}
    for line in codecs.open(filename, 'r', 'utf-8'):
        if idx != 0 and idx % 1000000 == 0:
            print(idx)
        idx += 1
        data = [int(x) for x in line.split()]
        if len(data) != 3:
            continue
        if data[0] != oldDoc:
            if len(currentWords) != 0:
                tfidfc.compute_vector_and_add(oldDoc, currentWords)
                currentWords = {}
            oldDoc = data[0]
        currentWords[data[1]] = data[2]
    if len(currentWords) != 0:
        tfidfc.compute_vector_and_add(oldDoc, currentWords)


def parse_tokens(docsfilename, idxfilename) :
    idx_dct = {}
    for line in codecs.open(idxfilename, 'r', 'utf-8') :
        data = line.split()
        idx_dct[data[0]] = int(data[1])
    
    currentwordcount = Counter()
    tfidfc = TFIDF_computation()

    for line in codecs.open(docsfilename, 'r', 'utf-8') :
        data = line.split()
        if len(data) == 0 :
            continue
        elif data[0] == '.I' :
            if len(currentwordcount) != 0 :
                docsize = 0
                for word in currentwordcount :
                    if word in idx_dct :
                        docsize += 1
                        tfidfc.add_word_usage(idx_dct[word],currentwordcount[word])
                tfidfc.add_doc_size(docsize)
                currentwordcount = Counter()
        elif data[0] == '.W' :
            continue
        else :
            currentwordcount.update(data)
    if len(currentwordcount) != 0 :
        docsize = 0
        for word in currentwordcount :
            if word in idx_dct :
                docsize += 1
                tfidfc.add_word_usage(idx_dct[word],currentwordcount[word])
        tfidfc.add_doc_size(docsize)
    
    tfidfc.init_storage("test.vectors", "")
    oldDoc = -1
    currentwordcount = Counter()
    
    for line in codecs.open(docsfilename, 'r', 'utf-8') :
        data = line.split()
        if len(data) == 0 :
            continue
        elif data[0] == '.I' :
            if len(currentwordcount) != 0 :
                currentwords = dict([(idx_dct[w],currentwordcount[w]) \
                    for w in currentwordcount if w in idx_dct])
                tfidfc.compute_vector_and_add(oldDoc, currentwords)
                currentwordcount = Counter()
            oldDoc = int(data[1])
        elif data[0] == '.W' :
            continue
        else :
            currentwordcount.update(data)
    if len(currentwordcount) != 0 :
        currentwords = dict([(idx_dct[w],currentwordcount[w]) \
            for w in currentwordcount if w in idx_dct])
        tfidfc.compute_vector_and_add(oldDoc, currentwords)


if __name__ == "__main__":
    #parse_bagofwords("data/docword.nytimes.txt")
    #parse_tokens('data/lyrl2004_tokens_test_sample.dat', 'data/stem.termid.idf.map.txt')
    reader = TFIDF_reader("test.vectors")
    vector1 = reader.read_idx(0)
    vector2 = reader.read_idx(10)
    dist = tfidf_cosine_distance(vector1, vector2)
    print(dist)
