#!/usr/bin/python3.2
# -*-coding:Utf-8 -*

import math
import numpy as np
import random as rnd

from tfidfStorage import TFIDF_reader
from tfidfStorage import tfidf_cosine_distance as cosdist
from cluster import Cluster

reader = TFIDF_reader("test.vectors")

# Number of tfidf vectors
npoint = reader.doc_nb
# Number of clusters
ncluster = 100

# Initialize centroids so that they are as far from one another as possible
# Centroids indices in tfidf_list
#centroids_idx = [0]
# Distance of each point to the closest cluster
#mindist = np.array([tfidfdct.cosdist(tfidf_list[0]) for tfidfdct in tfidf_list])
#for i in range(1, ncluster) :
#	max_idx = np.argmax(mindist)
#	centroids_idx.append(max_idx)
#	dist = np.array([tfidfdct.cosdist(tfidf_list[max_idx]) for tfidfdct in tfidf_list])
#	mindist = np.amin(np.vstack((mindist, dist)), 0)

#clusters = [Cluster(tfidf_list[c_idx]) for c_idx in centroids_idx]

# Inititalize centroids by hierarchical clustering on a sample
#nsample = math.ceil(0.05*npoint)
nsample = 5*ncluster
idxsample = rnd.sample(range(npoint), nsample)
docIdsample = [reader.read_idx(i)[0] for i in idxsample]
clusters_s = [Cluster(docIdsample[i], reader) for i in range(nsample)]
distmat = np.zeros((nsample, nsample))

print('Calculating initial clustroids')

for i in range(nsample) :
	distmat[i,i] = None
	for j in range(i+1,nsample) :
		dist = cosdist(clusters_s[i].clustroid, clusters_s[j].clustroid)
		distmat[i,j] = dist
		distmat[j,i] = dist

nmerged = nsample
while nmerged != ncluster :
	flatidx = np.nanargmin(distmat)
	i = flatidx//nsample
	j = flatidx%nsample
	clusters_s[i].merge(clusters_s[j])
	clusters_s[j] = None
	distmat[j,:] = None
	distmat[:,j] = None
	for k in range(nsample) :
		if clusters_s[k] != None and k != i :
			dist = cosdist(clusters_s[k].clustroid, clusters_s[i].clustroid)
			distmat[i,k] = dist
			distmat[k,i] = dist
	nmerged -= 1

clusters_s = [clu for clu in clusters_s if clu != None]

print('Done')
#for i, c in enumerate(clusters_s) :
#	print('Cluster {0} contains {1} points'.format(i+1, c.nvector()))
#	print('Document ids : {}'.format(c.vectorsid))
#	print('Radius : {}'.format(np.min(c.maxdist)))
#	print('Max distance : {}'.format(c.maxdist))

clusters = clusters_s

print('Starting kmeans')
nkmeanitr = 5
for k in range(nkmeanitr) :
	clusters = [Cluster(clu.clustroidid, reader) for clu in clusters]
	print('kmeans iteration : {0} / {1}'.format(k+1, nkmeanitr))
	for i in rnd.sample(range(npoint), npoint) :
		vector = reader.read_idx(i)
		# if vector is a clustroid, skip it
		if vector[0] in [clu.clustroidid for clu in clusters] :
			continue
		mindist = 2.0 # valid upper bound on cosine distance
		closestidx = None
		for i, clu in enumerate(clusters) :
			dist = cosdist(clu.clustroid, vector)
			if dist < mindist :
				mindist = dist
				closestidx = i
		clusters[closestidx].add(vector[0])
print('Done')

#with open('cl_kmeans','wb') as resfile :
#	Pickler(resfile).dump(clusters)















		
