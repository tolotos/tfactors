#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       correlate_cafe_count.py
#
#==============================================================================
from optparse import OptionParser
from Tfsuite.Parser.count import Count
from Tfsuite.Parser.cafe import Cafe
from Tfsuite.Classes.cluster import Cluster
import rpy
from ete2 import Tree
import copy
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog takes cafe and count output, maps the ancestral states onto the
        provided phylogeny and correlates the lineage reconstruction to each
        other. Output is printed to standard out'''
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-a', '--cafe', dest = 'cafe_in',
    help = 'Cafe input file', metavar='FILE', default = '')
cloptions.add_option('-t', '--tree', dest = 'tree',
    help = 'Phylogeny, must be identical to tree provided to count and cafe',
    metavar='FILE', default = '')
cloptions.add_option('-o', '--count', dest = 'count_in',
    help = 'Count input file', metavar='FILE', default = '')
(options, args) = cloptions.parse_args()
#==============================================================================

def cor(a,b,z):
    '''Takes two lists containing floats or integers and calculates the
       pearson correlation and significance using the rpy module.'''
    return rpy.r.cor(a,b, method=z)

def add_num_to_nodes(tree):
    '''Adds the attribute "num" to each node and assigns a value via postorder
       tree traversal. This is necessary, because the count output only maps
       internal nodes via postorder to numbers, but does not use the name.
       For example the internal node "Ciona" is referred to by count as "1".'''
    counter = 1
    for node in tree.traverse("postorder"):
        node.add_features(num=None)
        if node.is_leaf() == False:
            node.num = str(counter)
            counter += 1
    return tree

def add_cafe_and_count_to_nodes(tree):
    '''Adds the two attributes for the ancestral reconstructed values of count
       and cafe.'''
    for node in tree.traverse("postorder"):
        node.add_features(count=None,cafe=None)
    return tree

def map_cafe_to_tree(cafe, tree):
    return 0
def map_count_to_tree(count,tree):
    all = []
    for item in count:
        name, counts = item[0], item[1]
        cluster = Cluster(name, None)
        cluster.tree = copy.deepcopy(tree)
        for node in cluster.tree.traverse("postorder"):
            if node.is_leaf():
                node.count = counts[node.name]
            else:
                node.count = counts[node.num]
        all.append(cluster)
    return all


def get_lineage(node):
    counts= []
    while node:
        counts.append(node.count)
        node = node.up
    return counts


def main():
    cafe, count = Cafe(),Count()
    #cafe.load(options.cafe_in)
    count.load(options.count_in)
    tree = Tree(options.tree, format=1)
    tree = add_num_to_nodes(tree)
    tree = add_cafe_and_count_to_nodes(tree)

    clusters = map_count_to_tree(count,tree)

    for node in clusters[0].tree.traverse("postorder"):
        if node.is_leaf():
            print node.name, get_lineage(node)


if __name__ == '__main__':
    main()

