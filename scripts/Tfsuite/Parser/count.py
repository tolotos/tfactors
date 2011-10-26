#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       orthomcl.py


import sys

class Count:

    def __init__(self):
        self.name = ""
        self.clusters = {}

    def __iter__(self):
        #We are an iterable, so return our iterator
        for i in self.clusters:
            yield i, self.clusters[i]


    def write(self, orthomcl, species):
        '''Writes a Count input file. Species is a list, which contains all
           the species that should be included. Count needs this exact layout,
           therefore the \t and \n charcters are flushed directly.'''
        sys.stdout.write("family")
        for name in species:
            sys.stdout.write("\t"+name)
        for cluster in orthomcl:
            sys.stdout.write("\n"+str(cluster.name))
            for name in species:
                sys.stdout.write("\t"+str(cluster.counts[name]))


    def load(self, file):
        '''Parses a count ouput file. Each cluster or family is mapped to
           a dictionary that contains all nodes of the tree with the ancestral
           count that was reconstructed by the programm'''
        lines = open(file, 'r').readlines()
        nodes = None
        for line in lines:
            line = line.rstrip().split()
            if line[1] == "Family":
                nodes = line[2:]
            if nodes != None:
                sizes , name = line[1:],line[0]
                self.clusters[name] = dict(zip(nodes, sizes))





                #families = families.readlines()
                #groups = []
                #for line in families[1:]:
                    #line = line.rstrip()
                    #line = line.replace(' ', '_')
                    #line = line.split('\t')
                    #if line[0] == '#_Family':
                        #for element in line[1:]:
                            #groups.append([element, {}])
                    #else:
                        #for i in range(len(line)-1):
                            #groups[i][1][line[0]] = float(line[i+1])
                #counter = -2
                #for node in nodes:
                    #y = []
                    #for i in groups:
                        #y.append(i[0])
                    #if node.name not in y:
                        #groups[counter][0] = node.name
                        #counter += -1
                #groupsy = {}
                #for item in groups:
                    #groupsy[item[0]] = item[1]
                #for node in nodes:
                    #if node.name in groupsy:
                        #node.families = groupsy[node.name]
                #return nodes
