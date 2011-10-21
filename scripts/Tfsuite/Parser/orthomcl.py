#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       orthomcl.py
   



def load_cluster(self, cluster_file):
        cluster_file = open(cluster_file, "r").readlines()
        for line in cluster_file:
            cluster_name = line.split("\t")[0].split("(")[0]
            members = line.rstrip().split()
            members = members[3:]
            for member in members:
                member = member.split("(")[0][6:]
                if self.clusters.has_key(cluster_name):
                    self.clusters[cluster_name].members.append(self.proteins[member])
                else:
                    self.clusters[cluster_name] = Cluster(cluster_name,self.proteins[member])
