#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       orthomcl.py


from Tfsuite.Classes.cluster import Cluster

class Orthomcl:

    def __init__(self):
        self.clusters = {}

    def __iter__(self):
        #We are an iterable, so return our iterator
        for i in self.clusters:
            yield self.clusters[i]


    def load(self, file):
        file = open(file, "r").readlines()
        for line in file:
            name = line.split("\t")[0].split("(")[0]
            members = line.rstrip().split()
            members = members[3:]
            for member in members:
                member = member.split("(")[0][6:]
                if self.clusters.has_key(name):
                    self.clusters[name].members.append(member)
                else:
                    self.clusters[name] = Cluster(name,member)
