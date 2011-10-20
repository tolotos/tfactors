#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       proteine.py
   
class Protein:
    def __init__(self,gene_name):
        self.gene_name = gene_name
        self.seq = ""
        self.cluster = None
        self.species = None
        self.domains = []
        self.family = None
   
    def collapse_domains(self):
        domain_list = []
        for domain in self.domains:
            if len(self.domains) > 2:
                if len(domain_list) < 2:
                    domain_list.append(domain)
                elif domain_list[-1] == domain and domain_list[-2] == domain: 
                    pass
                else:
                    domain_list.append(domain)
        if len(domain_list) > 0:
            self.domains = domain_list
        else:
            pass
    def export_fasta(self):
        return ">"+self.species+"_"+self.gene_name+"\n", self.seq+"\n"
        
    def add_sequence(self,fasta):
		if self.gene_name in fasta.seqs:
			self.seq = fasta.seqs[self.gene_name]

