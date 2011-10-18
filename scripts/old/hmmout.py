#!/usr/bin/python


class Hmmout:
    
    def __init__(self,hmmout_file):
        self.hmmout = hmmout_file
        self.proteins = {}
    
    def get_proteins(self):
        return self.proteins
    
    def load_hmmout(self):
        hmmout = open(self.hmmout, "r").readlines()
        for line in hmmout:
            if not line.rstrip():
                continue
            elif line[0] == "#":
                continue
            else:
                line = line.rstrip().split()
                gene_name = line[0]
                pfam_id = line[5]
                domain = line[6]
                if self.proteins.has_key(gene_name):
                    self.proteins[gene_name].append(domain])
                else:
                    self.proteins[gene_name] = [domain]
    
