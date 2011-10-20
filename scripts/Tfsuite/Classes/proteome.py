#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2011 f_zimm01 <f_zimm01@EBBICORE4>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

class Proteome:
    def __init__(self,hmmout,fasta,arrangement,organisms):
        self.hmmout = hmmout
        self.proteins = {}
        self.fasta = fasta
        self.arrangement = arrangement
        self.organisms = organisms
        self.clusters = {}
        self.species_dic = {}
        #self.tree = tree
        
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
            

def main():
	
	return 0

if __name__ == '__main__':
	main()

