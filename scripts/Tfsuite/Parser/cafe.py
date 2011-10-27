#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       orthomcl.py

import glob
import sys
from ete2 import Tree

class Cafe:

    def __init__(self):
        self.name = ""
        self.clusters = {}

    def __iter__(self):
        #We are an iterable, so return our iterator
        for i in self.clusters:
            yield i, self.clusters[i]


    def write(self,orthomcl,species):
        '''Writes a cafe input file. Species is a list, which contains all
           the species that should be included. Cafe needs this exact layout,
           therefore the \t and \n charcters are flushed directly.'''
        sys.stdout.write("FAMILYDESC"+"\t"+"FAMILY")
        for name in species:
            sys.stdout.write("\t"+name)
        for cluster in orthomcl:
            sys.stdout.write("\n"+"---"+"\t"+str(cluster.name))
            for name in species:
                sys.stdout.write("\t"+str(cluster.counts[name]))

    def load(self,cafe_file):
        cafe_file = open(cafe_file, "r").readlines()
        for line in cafe_file:
            if line.startswith("O"):
                line = line.rstrip().split()
                self.clusters[line[0]] = [line[1],line[2],line[3]]

        #for name, cluster in self.clusters.items():
            #cluster.tree = cafe_dic[cluster.name][0]
            #cluster.p_value = float(cafe_dic[cluster.name][1])
            #cluster.branch_p = cafe_dic[cluster.name][2]




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
