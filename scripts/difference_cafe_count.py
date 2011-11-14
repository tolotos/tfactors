#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#       difference_cafe_count.py
#
#==============================================================================
from optparse import OptionParser
from Tfsuite.Parser.count import Count
from Tfsuite.Parser.cafe import Cafe
from Tfsuite.Classes.cluster import Cluster
from ete2a1 import *
import copy
import cPickle as pickle
#from rpy import r
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

def add_diff_to_nodes(tree):
    '''Adds the attribute "diff" to a tree. This is necessary to map the diff-
    erences between count and cafe reconstruction to the family tree of all
    clusters.Well, that makes sense now, what about tomorrow?'''
    for node in tree.traverse("postorder"):
        node.add_features(diff=0,total_count=0,total_cafe=0)
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
        #The deepcopy operation is the bottleneck of the programm, but each
        #cluster needs its own tree object!
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

def map_clusters_to_family(clusters, tree, families):
    '''This function takes all clusters and maps the individual clusters to the
    family tree. The tree must be provided as a ETE tree object and families
    contains a list of strings, the family names, that sould be produced.'''
    family_trees = {}
    for family in families:
        cur_tree = copy.deepcopy(tree)
        cur_tree = add_diff_to_nodes(cur_tree)
        for cluster in clusters:
            if cluster.family == family:
                for node in cluster.tree.traverse("postorder"):
                    if not node.is_leaf():
                        diff = abs(int(node.count) - int(node.cafe))
                        cur_node = cur_tree&node.name # Find node by name
                        cur_node.diff += diff
                        cur_node.total_count += int(node.count)
                        cur_node.total_cafe += int(node.cafe)
        family_trees[family] = cur_tree
    return family_trees

def plot_tree(family_trees):
    for i in family_trees:
        tree = family_trees[i]
        for node in tree.traverse():
            diff = TextFace(str(node.diff),
                            ftype='Verdana',
                            fsize=14,
                            fgcolor='#000000',
                            bgcolor=None,
                            penwidth=0,
                            fstyle='bold')
            tcount = TextFace(str(node.total_count),
                            ftype='Verdana',
                            fsize=10,
                            fgcolor='#000000',
                            bgcolor=None,
                            penwidth=0,
                            fstyle='italic')
            tcafe = TextFace(str(node.total_cafe),
                            ftype='Verdana',
                            fsize=10,
                            fgcolor='#000000',
                            bgcolor=None,
                            penwidth=0,
                            fstyle='normal')
            node.add_face(diff,column=0)
            node.add_face(tcount,column=0)
            node.add_face(tcafe,column=0)
        ts = TreeStyle()
        ts.show_leaf_name = True
        ts.title.add_face(TextFace(i, fsize=20), column=0)
        tree.render(i+".pdf",tree_style=ts)

def main():
    tree = Tree(options.tree, format=1)
    clusters = load_clusters(options.pickle)
    family_trees = map_clusters_to_family(clusters,tree,["other",
                                                         "HLH",
                                                         "Homeobox",
                                                         "bZIP",
                                                         "zf-C2H2",
                                                         "P53",
                                                         "NuclearFactors"])
    plot_tree(family_trees)

if __name__ == '__main__':
    main()
