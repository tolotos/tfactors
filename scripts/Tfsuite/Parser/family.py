#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       fasta.py


class Family:
    def __init__(self):
        self.families = []
        self.mapping = {}

    def __iter__(self):
        #We are an iterable, so return our iterator
        for i in self.mapping:
            yield i, self.mapping[i]

    def load(self,file):
        lines = open(file, "r").readlines()
        for line in lines:
            line = line.split()
            arrangement = line[0]
            family = line[1]
            self.mapping[arrangement] = family
            if family not in self.families:
                self.families.append(family)
