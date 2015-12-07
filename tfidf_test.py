#!/usr/local/bin/python3.5
# -*-coding:Utf-8 -*

import re
import math
from collections import Counter

def tf(word, textcount) :
	return textcount[word]/sum(textcount.values())

def idf(word, textcountlist) :
	ntextcont = sum(1 for textcount in textcountlist if word in textcount.keys())
	if ntextcont == 0 : # idf is theoretically infinite (n/0).
		return 0
	else :
		return math.log(len(textcountlist)/(ntextcont))

def tfidf(word,textcount,textcountlist) :
	return tf(word, textcount) * idf(word,textcountlist)

document1 = """Python is a 2000 made-for-TV horror movie directed by Richard
Clabaugh. The film features several cult favorite actors, including William
Zabka of The Karate Kid fame, Wil Wheaton, Casper Van Dien, Jenny McCarthy,
Keith Coogan, Robert Englund (best known for his role as Freddy Krueger in the
A Nightmare on Elm Street series of films), Dana Barron, David Bowe, and Sean
Whalen. The film concerns a genetically engineered snake, a python, that
escapes and unleashes itself on a small town. It includes the classic final
girl scenario evident in films like Friday the 13th. It was filmed in Los Angeles,
 California and Malibu, California. Python was followed by two sequels: Python
 II (2002) and Boa vs. Python (2004), both also made-for-TV films."""

document2 = """Python, from the Greek word (πύθων/πύθωνας), is a genus of
nonvenomous pythons[2] found in Africa and Asia. Currently, 7 species are
recognised.[2] A member of this genus, P. reticulatus, is among the longest
snakes known."""

document3 = """The Colt Python is a .357 Magnum caliber revolver formerly
manufactured by Colt's Manufacturing Company of Hartford, Connecticut.
It is sometimes referred to as a "Combat Magnum".[1] It was first introduced
in 1955, the same year as Smith &amp; Wesson's M29 .44 Magnum. The now discontinued
Colt Python targeted the premium revolver market segment. Some firearm
collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy
Thompson, Renee Smeets and Martin Dougherty have described the Python as the
finest production revolver ever made."""

doclist = [document1,document2,document3]
textcountlist = []
for doc in doclist :
	words = re.findall('\w+', doc.lower())
	textcountlist.append(Counter(words))

scores = []
for i, textcount in enumerate(textcountlist) :
	print('Document {}'.format(i+1))
	scores.append({word: tfidf(word,textcount,textcountlist) for word in textcount.keys()})
	score_sorted = sorted(scores[i].items(), key=lambda x: x[1], reverse=True)
	for word, score in score_sorted[:3] :
		print('\tWord : {}, tfidf : {}'.format(word, score))













