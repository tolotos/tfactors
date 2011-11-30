#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       cyto.py

import glob
import sys

class Cyto:

    def __init__(self):
        self.name = ""
        self.nodes = {}
        self.interaction_type = None

    def __iter__(self):
        #We are an iterable, so return our iterator
        for i in self.clusters:
            yield i, self.clusters[i]


    def load(self,cyto_file):
        cyto_file = open(cyto_file, "r").readlines()
        for line in cyto_file:
            line = line.split()
            self.nodes[line[0]] = line[2]
            if self.interaction_type == None:
                self.interaction_type = line[1]
            else:
                if line[1] != self.interaction_type:
                    print "More then one interaction type detected!"

    def edges(self):
        from_nodes = []
        to_nodes = []
        for node in self.nodes:
            from_nodes.append(node)
            to_nodes.append(self.nodes[node])
        return from_nodes, to_nodes
