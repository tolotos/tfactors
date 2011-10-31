#!/usr/bin/env python2.7
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
import cPickle as pickle
from rpy import r
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
cloptions.add_option('-p', '--pickle', dest = 'pickle',
    help = 'Filename for the pickled clusters', metavar='FILE',
    default = 'pickled_orthomcl_clusters.p')
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

def map_cafe_to_tree(clusters, cafe, tree):
    '''Takes the tree objects and family p-value for each cluster provided
       by the cafe parser and maps the reconstructed counts to the nodes of
       a tree for each cluster. Some postprocessing, like parsing the tree
       object is done in here, which should be moved into the parser at some
       point. This should result in a similar small function as
       map_count_to_tree provides.'''
    for cluster in clusters:
        c_counts = {}
        cafe_tree = cafe.clusters[cluster.name][0]
        cafe_tree = Tree(cafe_tree+";",format=1)
        cafe_tree = add_num_to_nodes(cafe_tree)
        for node in cafe_tree.traverse("postorder"):
            if node.is_leaf():
                a = node.name.split("_")
                c_counts[a[0]] = a[1]
            else:
                a = node.name[1:]
                c_counts[node.num] = a
        for node in cluster.tree.traverse("postorder"):
            if node.is_leaf():
                node.cafe = c_counts[node.name]
            else:
                node.cafe = c_counts[node.num]
    return clusters

def map_count_to_tree(clusters,count,tree):
    '''Takes the parsed count ouput provided and maps it onto the nodes
       of the tree for each cluster (node.count).'''
    for cluster in clusters:
        counts = count.clusters[cluster.name]
        #print name, counts
        cluster.tree = copy.deepcopy(tree)
        for node in cluster.tree.traverse("postorder"):
            if node.is_leaf():
                node.count = counts[node.name]
            else:
                node.count = counts[node.num]
    return clusters

def get_lineage(node):
    '''Walks back from node to root and returns two lists, where each list
       contains the reconstructed states by cafe or count respectivly. These
       two lists can be used by the cor function to correlate the results.'''
    count= []
    cafe = []
    while node:
        count.append(int(node.count))
        cafe.append(int(node.cafe))
        node = node.up
    return count, cafe

def get_distance_to_root(node):
    '''Walks back from node to root and returns the distance.'''
    dist = 0
    while node:
        dist +=1
        node = node.up
    return dist

def load_clusters(clusters):
    '''Loads clusters from pickled objects.
       The count and cafe results are added to the pickled clusters and
       can then be processed further. (Analysis, new pickling.)'''
    clusters = pickle.load(open(clusters,"r"))
    cafe, count = Cafe(),Count()
    cafe.load(options.cafe_in)
    count.load(options.count_in)
    tree = Tree(options.tree, format=1)
    add_num_to_nodes(tree)
    add_cafe_and_count_to_nodes(tree)
    clusters = map_count_to_tree(clusters,count,tree)
    clusters = map_cafe_to_tree(clusters,cafe,tree)
    return clusters

def main():
    clusters = load_clusters(options.pickle)
    cluster = clusters.clusters["ORTHOMCL422"]
    cl_diff = []
    cl_dist = []
    print cluster.name
    for node in cluster.tree.traverse("postorder"):
        if not node.is_leaf():
            diff = abs(int(node.count) - int(node.cafe))
            dist = get_distance_to_root(node)
            cl_diff.append(diff)
            cl_dist.append(dist)
    print cl_diff
    print cl_dist
    r.png("test.png", width=500, height=500)
    r.plot(x=cl_dist, y=cl_diff, xlab="Distance", ylab="Difference")
    r.dev_off()

if __name__ == '__main__':
    main()
