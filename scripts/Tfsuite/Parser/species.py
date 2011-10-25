#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py



class SpeciesMapping:

    def __init__(self):
        self.specmap = {}

    def __iter__(self):
    #We are an iterable, so return our iterator
        for i in self.specmap:
            yield i, self.specmap[i]

    def load(self, file):
        organisms = open(file, "r").readlines()
        for line in organisms:
            line = line.rstrip().split()
            name = line[0].replace(":","_")
            self.specmap[name] = line[1]

    def all(self):
        species = {}
        for i in self.specmap:
            if species.has_key(self.specmap[i]) == False:
                species[self.specmap[i]] = 0
        return species
