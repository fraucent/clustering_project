#!/usr/local/bin/python3.5
# -*-coding:Utf-8 -*

import math
from pickle import Pickler, Unpickler
from operator import itemgetter
from tfidf import TfidfDict

# Number of clusters
k = 5

class Cluster :
	def __init__(self, centroid) :
		self.sumpoint = centroid
		self.npoint = 1
	def centroid(self) :
		return sumpoint/npoint
	def add(self, tfidfdct) :
		self.sumpoint += tfidfdct
		self.npoint += 1

with open('reuter_tfidf','rb') as reutertfidf :
	tfidf_list = Unpickler(reutertfidf).load()

centroids_idx = [0]
for i in range(1, k) :
	max_dist = 0
	max_idx = None
	print(tfidf_list[61])
	for j, tfidfdct in enumerate(tfidf_list) :
		if j not in centroids_idx :
			min_dist = tfidfdct.mindist([tfidf_list[idx] for idx in centroids_idx])
			if min_dist == 1 : # max possible cosine distance
				max_idx = j
				break
			elif min_dist > max_dist :
				max_dist = min_dist
				max_idx = j
	centroids_idx.append(max_idx)

