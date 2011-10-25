#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       fasta.py


class Fasta:
    def __init__(self):
        self.seqs = {}

    def __iter__(self):
        #We are an iterable, so return our iterator
        for i in self.seqs:
            yield i, self.seqs[i]

    def load(self,file):
        lines = open(file, "r").readlines()
        for line in lines:
            if line[0] == ">":
                name = line[1:].rstrip()
                self.seqs[name] = ""
            else:
                self.seqs[name] += line.rstrip()
