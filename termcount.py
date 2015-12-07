#!/usr/local/bin/python3.5
# -*-coding:Utf-8 -*

import re
from html.parser import HTMLParser
from collections import Counter
from pickle import Pickler

class CountingParser(HTMLParser) :
	valid_tags = ['reuters', 'topics', 'title', 'body']
	def __init__(self, stopwords = []) :
		self.stopwords = stopwords
		self.doclist = []
		self.currenttopics = []
		self.currentcount = Counter([])
		self.currenttitle = ''
		self.currenttag = ''
		HTMLParser.__init__(self)
	def handle_starttag(self, tag, attrs) :
		if tag in CountingParser.valid_tags :
			self.currenttag = tag
			print(tag)
		if tag == 'reuters' :
			self.currenttopics = []
			self.currentcount = Counter([])
	def handle_endtag(self, tag) :
		if tag in CountingParser.valid_tags :
			self.currenttag = ''
		if tag == 'reuters' :
			if len(self.currenttopics) > 0 :
				self.doclist.append((self.currenttopics, self.currentcount))
				#if len(self.currentcount) == 0 :
				#	print(self.currenttitle)
			#self.currenttopics = []
			#self.currentcount = Counter([])
			#self.currenttitle = ''
	def handle_data(self, data) :
		if self.currenttag == 'topics' :
			self.currenttopics.append(data)
		elif self.currenttag in ['title', 'body'] :
			if self.currenttag == 'title' :
				self.currenttitle = data
			tokens = re.findall('\w+', data.lower())
			words = [] # list of words that do not include numbers
			for token in tokens :
				if re.search('[a-z]', token) and token not in stopwords :
					words.append(token)
			if len(words) == 0 :
				print('zero words')
				print(data)
			self.currentcount.update(words)

with open('data/stopwords') as stwordfile :
	stopwords = stwordfile.read().split()
	
parser = CountingParser(stopwords)
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
for fname in reuterfnames :
	reuterfile = open(fname, 'r')
	parser.feed(reuterfile.read())
	reuterfile.close()

with open('reuter_parsed','wb') as reuterp :
	Pickler(reuterp).dump(parser.doclist)


