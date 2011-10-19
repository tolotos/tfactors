#!/usr/bin/python

from optparse import OptionParser
import os
import glob
import sys
#=============================================================================
#Command line options=========================================================
#=============================================================================

usage = 'usage: %prog [options]'
desc="""%prog takes domain arrangment as subfamilies and maps them to sequences and species"""
        
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-f', '--arrangment2family', dest = 'arrangment2family',
    help = 'Required arrangement to family mapping', metavar='FILE',
    default = '/home/fabian/Dropbox/uni/Master/FM_1_TF/data/input/arrangement2family')
cloptions.add_option('-m', '--hmmout', dest = 'hmmout',
    help = 'Required hmmout file', metavar='FILE',
    default = '/home/fabian/Dropbox/uni/Master/FM_1_TF/data/input/TF.sequences.28092010.hmmout')
cloptions.add_option('-s', '--sequences', dest = 'sequences',
    help = 'Required fasta file containing all sequences', metavar='FILE',
    default = '/home/fabian/Dropbox/uni/Master/FM_1_TF/data/input/TF.sequences.28092010.fasta')
cloptions.add_option('-o', '--organisms', dest = 'organisms',
    help = 'Required mapping from sequence names to species', metavar='FILE',
    default = '/home/fabian/Dropbox/uni/Master/FM_1_TF/data/input/speciesMapping')    
(options, args) = cloptions.parse_args()

#=============================================================================

hmmout = options.hmmout
fasta = options.sequences
organisms = options.organisms
arrangement = options.arrangment2family


#=============================================================================

class Proteome:
    def __init__(self,hmmout,fasta,arrangement,organisms):
        self.hmmout = hmmout
        self.proteins = {}
        self.fasta = fasta
        self.arrangement = arrangement
        self.organisms = organisms
        self.clusters = {}

    def load_hmmout(self):
        hmmout = open(self.hmmout, "r").readlines()
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
                self.proteins[gene_name] = Proteine(gene_name)
                self.proteins[gene_name].domains.append(domain)
    
    def load_fasta(self):
        sequences = open(self.fasta, "r").readlines()
        for line in sequences:
            if line[0] == ">":
                name = line[1:].rstrip()
                if name.find(":"):
                    name = name.replace(":","_")
            else:
                if self.proteins.has_key(name):
                    self.proteins[name].seq += line.rstrip()
                else:
                    pass

    def load_arrangement(self):
        arrag_dict = {}
        for name, protein in self.proteins.items():
                protein.collapse_domains()
        arrangement = open(self.arrangement, "r").readlines()
        for line in arrangement:
           line = line.split()
           arrag = "".join(line[0].split(";"))
           family = line[1]
           arrag_dict[arrag] = family
        for name, protein in self.proteins.items():
            prodom_string = "".join(protein.domains)
            if arrag_dict.has_key(prodom_string):
                protein.family = arrag_dict[prodom_string]
    
    def load_species(self):
        mapping = {}
        organisms = open(self.organisms, "r").readlines()
        for line in organisms:
            line = line.rstrip().split()
            name = line[0].replace(":","_")
            if self.proteins.has_key(name):
                self.proteins[name].species = line[1]    
    
    def find_proteins_by(self, format, queries):
        search_results = {}
        if format == "family":
            objects = self.proteins.items()
        elif format == "cluster":
            objects = self.clusters.items()
        elif format == "species":
            objects = self.proteins.items()

        for query in queries:
            search_results.setdefault(query,[])
            for name, sobject in objects:
                if sobject.family == query:
                    search_results[query].append(sobject)
        return search_results
    
    def load_cluster(self, clusters):
        for cluster_file in clusters:
            cluster_file = open(cluster_file, "r").readlines()
            for line in cluster_file:
                if line[0] == ">":
                    name = line[1:].rstrip()
                    name = name.split()[1]
                else:
                    line = line.split()
                    gene_name = line[2][1:][:-3]
                    clust_name = self.proteins[gene_name].family+"_"+name
                    if self.clusters.has_key(clust_name):
                        self.clusters[clust_name].members.append(self.proteins[gene_name])
                    else:
                        self.clusters[clust_name] = Cluster(clust_name,self.proteins[gene_name])
        for name, cluster in self.clusters.items():
             cluster.add_family()

class Species:
    def __init__(self,name):
        self.name = name
        self.families = {}
    
    def import_families(self,proteome):
        for name, protein in proteome.proteins.items():
            self.families.setdefault(protein.family,0) 

class Proteine:
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

class Cluster:
    def __init__(self, name,member):
        self.name = name
        self.count = 0
        self.members = [member]
        self.family = None
    
    def add_family(self):
        self.family = self.members[0].family

#============================================================================
def prot_to_spec(proteome):
    spec_dic = {}
    
    for name, protein in proteome.proteins.items():
        if spec_dic.has_key(protein.species):
            if spec_dic[protein.species].families.has_key(protein.family):
                spec_dic[protein.species].families[protein.family] +=1
        else:
            spec_dic[protein.species] = Species(protein.species)
            spec_dic[protein.species].import_families(proteome)
    return spec_dic
#============================================================================
proteome = Proteome(hmmout, fasta, arrangement,organisms)

proteome.load_hmmout()
proteome.load_fasta()
proteome.load_arrangement()
proteome.load_species()
#proteome.load_cluster(clusters)


for name, protein in proteome.proteins.items():
    print protein.species


#sys.stdout.write("FAMILYDESC"+"\t"+"FAMILY")
#for name, species in test.items():
#    sys.stdout.write("\t"+species.name)

#counts = []
#for name, species in test.items():
#    counts.append((zip(*species.families.items())[1]))
#    names = species.families.keys()

#counter = 0
#counts = zip(*counts)
#for name in names:
#    sys.stdout.write("\n"+"---"+"\t"+str(name))
#    for i in counts[counter]:
#        sys.stdout.write("\t"+str(i))
#    counter +=1

