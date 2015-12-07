#!/usr/local/bin/python3.5
# -*-coding:Utf-8 -*

from pickle import Pickler, Unpickler
import math

class TfidfDict(dict) :
	def __add__(self, tfidfdct) :
		sumdct = TfidfDict(self.items())
		for word in tfidfdct.keys() :
			if word in sumdct.keys() :
				sumdct[word] += tfidfdct[word]
			else :
				sumdct[word] = tfidfdct[word]
		return sumdct
	def __iadd__(self, tfidfdct) :
		for word in tfidfdct.keys() :
			if word in self.keys() :
				self[word] += tfidfdct[word]
			else :
				self[word] = tfidfdct[word] 
		return self
	def __mul__(self, scalar) :
		muldct = TfidfDict(self.items())
		for word in muldct.keys() :
			muldct[word] *= scalar
		return muldct
	def __rmul__(self, scalar) :
		return self.__mul__(scalar)
	def __truediv__(self, scalar) :
		return self.__mul__(1/scalar)
	def cosdist(self, tfidfdct) :
		shared_words = [word for word in self.keys() if word in tfidfdct.keys()]
		dotprod = sum([self[word]*tfidfdct[word] for word in shared_words])
		return 1 - dotprod / math.sqrt(sum(tfidf**2 for tfidf in self.values()) *
			sum(tfidf**2 for tfidf in tfidfdct.values()))
	def closest(self, list_tdct) :
		min_dist = 2 # cos distance always <= 1 !
		closest_idx = -1
		for i, tfidfdct in enumerate(list_tdct) :
			d = self.cosdist(tfidfdct)
			if d < min_dist :
				min_dist = d
				closest_idx = i
		return closest_idx
	def mindist(self, list_tdct) :
		return self.cosdist(list_tdct[self.closest(list_tdct)])

# Test TfidfDict class (special methods)
#d1 = TfidfDict([('alpha',1), ('beta',2), ('dzeta',3)])
#d2 = TfidfDict([('beta',1), ('dzeta',2), ('epsilon',3)])
#print('Sum of the following two tfidf vectors')
#print('d1 : {}'.format(d1))
#print('d2 : {}'.format(d2))
#d1 += d2
#print('d1 : {}'.format(d1))
#print('d2 : {}'.format(d2))
#print('is computed as')
#print(d1+d2)
#print(d2*2)
#print(3*d1)
#print(d1/4)


with open('reuter_parsed','rb') as reuterp :
	doclist = Unpickler(reuterp).load()

len_doclist = len(doclist)

# For each term, compute the number documents containing it
doccount = dict()
for doc in doclist :
	for word in doc[1].keys() :
		if word in doccount.keys() :
			doccount[word] += 1
		else :
			doccount[word] = 1

#print(len(doccount))
#print(doccount['reuter'])

# For each document, compute the tfidf vector as a TfidfDict object
tfidf_list = []
for doc in doclist :
	tfidf_dict = TfidfDict()
	for word in doc[1].keys() :
		tf = doc[1][word]/sum(doc[1].values())
		idf = math.log(len_doclist/(doccount[word]))
		tfidf_dict[word] = tf*idf
	tfidf_list.append(tfidf_dict)

# Write the list of tfidf vectors on the file 'reuter_tfidf'
with open('reuter_tfidf','wb') as reutertfidf :
	Pickler(reutertfidf).dump(tfidf_list)

# Test : print tfidf of the words of a few documents
#for i, tfidf_dict in enumerate(tfidf_list[:3]) :
#	print('Document {}'.format(i+1))
#	tfidf_sorted = sorted(tfidf_dict.items(), key=lambda x: x[1], reverse=True)
#	for word, tfidf in tfidf_sorted :
#		print('\tWord : {}, tfidf : {}'.format(word, tfidf))
