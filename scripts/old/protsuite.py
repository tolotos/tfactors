#!/usr/bin/python

from ete2 import *
import os
import glob
import sys
import copy
import re


class Proteome:
    def __init__(self,hmmout,fasta,arrangement,organisms,tree):
        self.hmmout = hmmout
        self.proteins = {}
        self.fasta = fasta
        self.arrangement = arrangement
        self.organisms = organisms
        self.clusters = {}
        self.species_dic = {}
        self.tree = tree

    def load_tree(self):
        self.tree = PhyloTree(self.tree, format=3)


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
                if self.species_dic.has_key(line[1]):
                    pass
                else:
                    self.species_dic[line[1]] = 0
    
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
    
    def load_cluster(self, cluster_file):
        cluster_file = open(cluster_file, "r").readlines()
        for line in cluster_file:
            cluster_name = line.split("\t")[0].split("(")[0]
            members = line.rstrip().split()
            members = members[3:]
            for member in members:
                member = member.split("(")[0][6:]
                if self.clusters.has_key(cluster_name):
                    self.clusters[cluster_name].members.append(self.proteins[member])
                else:
                    self.clusters[cluster_name] = Cluster(cluster_name,self.proteins[member])
    
    def load_cafe(self,cafe_file):
        cafe_dic = {}
        cafe_file = open(cafe_file, "r").readlines()
        for line in cafe_file:
            if line[0] == "O":
                line = line.rstrip().split()
                #print line[3]#,line[2],line[3]
                cafe_dic[line[0]] = [line[1],line[2],line[3]]
        for name, cluster in self.clusters.items():
            cluster.tree = cafe_dic[cluster.name][0]
            cluster.p_value = float(cafe_dic[cluster.name][1])
            cluster.branch_p = cafe_dic[cluster.name][2]
    
    def map_cafe_tree(self, cafe_file):
        cafe_file = open(cafe_file, "r").readlines()
        for line in cafe_file:
            if line[0:5] == "# IDs":
                line = line.split(":")
                tree = Tree(line[1]+";",format=1)
        for node in tree.traverse("postorder"):
            node.add_features(ident=None,branch_p="na",position=None,count=0)
            if node.is_leaf():
                pos = node.name.find("<")
                match= re.search("\d+", node.name)
                match= match.group(0)
                node.ident = match
                node.name = node.name[:pos]
            if not node.is_leaf():
                if node.up:
                    child_1 = node.children[0].name
                    child_2 = node.children[1].name
                    ancestor = self.tree.get_common_ancestor(child_1, child_2)
                    match= re.search("\d+", node.name)
                    match= match.group(0)
                    node.ident = match
                    node.name = ancestor.name
        self.tree = tree

    def map_cafe_position(self,cafe_file):
        cafe_file = open(cafe_file, "r").readlines()
        for line in cafe_file:
            if re.search("node ID",line):
                branch_order = line.rstrip().split(":")[2]
                branch_order= branch_order.split()
                counter = 0
                for item in branch_order:
                    item = eval(item)
                    for node in self.tree.traverse():
                        if node.up:
                            if int(node.ident) == int(item[0]):
                                node.position = counter
                                counter += 1
                            elif int(node.ident) == int(item[1]):
                                node.position = counter                                
                                counter += 1
        return self.tree
            
        
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
        self.counts = {}
        self.members = [member]
        self.family = None
        self.tree = None
        self.p_value = None
        self.branch_p = None
        self.ancestral_counts = {}
        self.species_tree = None
    
    def add_family(self):
        self.family = self.members[0].family

    def add_cluster_to_members(self):
            for protein in self.members:
                protein.cluster = self
                
    def create_counts_dic(self,proteome):
        self.counts = copy.deepcopy(proteome.species_dic)

    def add_counts(self):
        for protein in self.members:
            self.counts[protein.species] += 1
    
    def add_ancestral_dic(self):
        for node in self.species_tree.traverse():
            self.ancestral_counts[node.name] = 0
    
    def parse_ancestral_counts(self):
        self.tree = Tree(self.tree+";",format=8)
        for node in self.tree.traverse("postorder"):
            pos = node.name.find("_")
            count = node.name[pos+1:]
            if node.is_leaf():
                node.name = node.name[:pos]
                self.ancestral_counts[node.name] = count
                for species_node in self.species_tree.traverse():
                    if species_node.name == node.name:
                        species_node.count = count
            if not node.is_leaf():
                if node.up:
                    child_1 = node.children[0].name
                    child_2 = node.children[1].name
                    ancestor = self.species_tree.get_common_ancestor(child_1, child_2)
                    node.name = ancestor.name
                    self.ancestral_counts[node.name] = count
                    for species_node in self.species_tree.traverse():
                        if species_node.name == node.name:
                            species_node.count = count
            
    def add_tree(self,tree):
        self.species_tree = copy.deepcopy(tree)
    
    def map_branch_p(self,p_value):
        if self.p_value <= float(p_value):
            branch_list = eval(self.branch_p)
            counter = 0
            tmp = []
            for item in branch_list:
                    tmp.append(item[0])
                    tmp.append(item[1])
            branch_list = tmp
            counter = 0
            for item in branch_list:                        
                if float(item) <= float(p_value):
                    for node in self.species_tree.traverse():
                        if node.position == counter:
                            #print node.name, counter, item
                            node.branch_p = float(item)
                counter += 1
        else:
            pass
            #print "Sorry, family has no sig. p-value"

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




