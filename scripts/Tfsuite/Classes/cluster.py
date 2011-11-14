#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Cluster.py

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
        #self.cor = None


    def add_proteins(self, hmmout):
        '''Adds protein objects from hmmout to a cluster, members at first are
           stored as strings "gene_name" from orthomcl input and then are
           replaced by protein objects provided by the hmmout input file'''
        tmp_objects = []
        for i in self.members:
            tmp_objects.append(hmmout.proteins[i])
        self.members = tmp_objects

    def add_family(self):
        '''Adds the family to the current clusters. The families from the
        members are used. If all members of the cluster are also members of the
        same family, the cluster is assigned the family of all members'''
        families = []
        for member in self.members:
            families.append(member.family)
        if len(set(families)) == 1:
            self.family = families[0]

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


def main():

    return 0

if __name__ == '__main__':
    main()

