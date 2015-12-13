#!/usr/bin/python3.2
# -*-coding:Utf-8 -*

import numpy as np
from tfidfStorage import tfidf_cosine_distance as cosdist
from tfidfStorage import TFIDF_reader

class Cluster :
	def __init__(self, clustroidid, reader) :
		self.clustroidid = clustroidid
		self.vectorsid = [clustroidid]
		self.maxdist = [0]
		self.reader = reader
		self.clustroid = self.reader.read_docId(clustroidid)
	def nvector(self) :
		return len(self.vectorsid)
	def add(self, docid) :
		vector = self.reader.read_docId(docid)
		maxdistvector = 0
		for i, vid in enumerate(self.vectorsid) :
			currvec = self.reader.read_docId(vid)
			currdist = cosdist(vector, currvec)
			if currdist > self.maxdist[i] :
				self.maxdist[i] = currdist
			if currdist > maxdistvector :
				maxdistvector = currdist
		self.vectorsid.append(docid)
		self.maxdist.append(maxdistvector)
		newclustroidid = self.vectorsid[np.argmin(self.maxdist)]
		if newclustroidid != self.clustroidid :
			self.clustroidid = newclustroidid
			self.clustroid = self.reader.read_docId(newclustroidid)
	def merge(self, cluster) :
		selfvectors = [self.reader.read_docId(i) for i in self.vectorsid]
		clustervectors = [cluster.reader.read_docId(i) for i in cluster.vectorsid]
		clustermaxdist = cluster.maxdist
		for i, selfvec in enumerate(selfvectors) :
			for j, clustervec in enumerate(clustervectors) :
				dist = cosdist(selfvec, clustervec)
				if dist > self.maxdist[i] :
					self.maxdist[i] = dist
				if dist > clustermaxdist[j] :
					clustermaxdist[j] = dist
		self.vectorsid.extend(cluster.vectorsid)
		self.maxdist.extend(clustermaxdist)
		newclustroidid = self.vectorsid[np.argmin(self.maxdist)]
		if newclustroidid != self.clustroidid :
			self.clustroidid = newclustroidid
			self.clustroid = self.reader.read_docId(newclustroidid)

#class BFRCluster(Cluster) :
#	def __init__(self, centroid) :
#		self.sumsqpoint = centroid**2 # tfidf class **
#		Cluster.__init__(self, centroid)
#	def add(self, tfidfdct) :
#		self.sumsqpoint += tfidfdct**2
#		Cluster.add(self, tfidfdct)
#	def mdist(self, tfidfdct) :
#		variance = (self.sumsqpoint/self.npoint) - (self.sumpoint/self.npoint)**2 # tfidf class -
#		
		
