#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#       timetree.py
#
#==============================================================================
from optparse import OptionParser
from ete2a1 import *
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog takes a newick tree and queries timetree to date the splits.
        Trees can be produced using the mean or median estimate. In addition
        a CSV can be produced listing the splits.'''
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-t', '--tree', dest = 'tree',
    help = 'Phylogeny, must be provided as a newick tree',
    metavar='FILE', default = '')
cloptions.add_option('-m', '--mode', dest = 'mode',
    help = 'Mean == 0, median == 1 . Default is 0.',
    metavar='FILE', default = '0')
cloptions.add_option('-o', '--output', dest = 'output',
    help = 'basename for the output',
    metavar='FILE', default = '')
cloptions.add_option('-l', '--list', dest = 'list',
    help = 'If specified a csv is produced containing the splittimes',
    metavar='FILE', default = '')
(options, args) = cloptions.parse_args()
#==============================================================================

def query_timetree(taxon_a,taxon_b):
    '''Mechanize is used to query the webinterface of timetree with two taxa
       and returns the result page after submiting the query form.'''
    br = Browser()
    br.addheaders = [('User-agent', 'Firefox')]
    br.set_handle_robots( False )
    br.open("http://timetree.org")
    br.select_form(name="query_frm")
    br['taxon_a'] = taxon_a
    br['taxon_b'] = taxon_b
    resp = br.submit()
    html = resp.get_data()
    return html

def extract_time(html):
    '''BeautifulSoup html parser is used to extract the estimated times from
       timetree html provided by query_timetree() and stores it in a dict.'''
    results = {"mean": None, "median": None, "expert": None}
    soup = BeautifulSoup(html)
    summary = soup.find("table")
    if summary != None:
        for row in summary.findAll('tr'):
            col = row.findAll('td')
            time = float(str(col[1].contents[0]).split()[0])
            if col[0].contents[0] == "Mean:":
                results["mean"] = time
            elif col[0].contents[0] == "Median:":
                results["median"] = time
            elif col[0].contents[0] == "Expert Result:":
                results["expert"] = time
    #else:
       # print "Sorry entry could not be found in timetree!"
    return results

def inner_type(node):
    '''Determines the three possible inner node types in regard to the children:
       node has two leafs (type 0), node has one leaf and one other inner node
       (type 1) or two inner nodes (type 2). If a leaf is supplied it returns
       False.'''
    left, right = node.get_children()[0], node.get_children()[1]
    if left.is_leaf():
        if right.is_leaf():
            return 0
        else:
            return 1
    if not left.is_leaf():
        if right.is_leaf():
            return 1
        if not right.is_leaf():
            return 2

def select_age(age):
    '''Selects the used aged in the order expert, median, mean. If no times
       could be extracted it returns a dist of 1.0, the standard that is used
       by ETE.'''
    if age["expert"] != None:
        return age["expert"]
    elif age["median"] != None:
        return age["median"]
    elif age["mean"] != None:
        return age["mean"]
    else:
        return 1.0

def date_node(taxon_a, taxon_b):
    '''Takes two taxa and computes the split provided by timetree'''
    html = query_timetree(taxon_a,taxon_b)
    age = extract_time(html)
    return select_age(age)

def date_tree(tree):
    '''Dates each internal node of a provided newick tree in format 1. The tree
       is traversed using "postorder". Three internal node cases are beeing
       distinguished by the inner_type() function. For type 0, both children
       are leafes, thus the age of the node is the divergence time of the two
       leafes. For type 1, only child A is a leaf the other child B is an
       internal node. The age of the node is the divergence time of child A and
       the first leaf that descents from child B. For type 2 both children are
       internal nodes, the age of the node is the divergence time of the first
       leaf found that descents of child A and child B respectivly.'''
    tree = Tree(tree, format=1)
    for node in tree.traverse("postorder"):
        if not node.is_root() and not node.is_leaf():
            left, right = node.get_children()[0], node.get_children()[1]
            if inner_type(node) == 0:
                node.dist = date_node(left.name,right.name)
            elif inner_type(node) == 1:
                if left.is_leaf():
                    right = right.get_leaf_names()[0]
                    node.dist = date_node(left.name, right)
                elif right.is_leaf():
                    left = left.get_leaf_names()[0]
                    node.dist = date_node(left, right.name)
            elif inner_type(node) == 2:
                left = left.get_leaf_names()[0]
                right = right.get_leaf_names()[1]
                node.dist = date_node(left, right)
    return tree

def plot_tree(tree):
    '''Plots a tree object with all nodes and leafes labeld by name and
       distance.'''
    for node in tree.traverse():
        name = TextFace(str(node.name),
                        ftype='Verdana',
                        fsize=14,
                        fgcolor='#000000',
                        bgcolor=None,
                        penwidth=0,
                        fstyle='bold')
        dist = TextFace(str(node.dist),
                        ftype='Verdana',
                        fsize=10,
                        fgcolor='#000000',
                        bgcolor=None,
                        penwidth=0,
                        fstyle='bold')
        node.add_face(name,column=0)
        node.add_face(dist,column=0)
    ts = TreeStyle()
    ts.title.add_face(TextFace("All species, with timetree dates", fsize=20), column=0)
    tree.show(tree_style=ts)


dated_tree = date_tree(options.tree)
plot_tree(dated_tree)



