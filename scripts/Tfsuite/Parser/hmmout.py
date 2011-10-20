#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       hmmout.py


from Tfsuite.Classes.protein import Protein

class Hmmout:
	
	def __init__(self):
		self.proteins = {}
		
	def __iter__(self):
		#We are an iterable, so return our iterator
		for i in self.proteins:
			yield self.proteins[i]

	def load(self, file):
	    hmmout = open(file, "r").readlines()
	    for line in hmmout:
			if not line.rstrip():
				continue
			elif line[0] == "#":
				continue
			else:
				line = line.rstrip().split()
				gene_name = line[0].replace(":","_")
				pfam_id = line[5]
				domain = line[6]
			if self.proteins.has_key(gene_name):
				self.proteins[gene_name].domains.append(domain)
			else:
				self.proteins[gene_name] = Protein(gene_name)
				self.proteins[gene_name].domains.append(domain)
	
