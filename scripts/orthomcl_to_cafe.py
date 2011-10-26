#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  orthomcl_to_cafe.py
#
#==============================================================================
from optparse import OptionParser
from Tfsuite.Parser.species import SpeciesMapping
from Tfsuite.Parser.cafe import Cafe
import os
import glob
import copy
import cPickle as pickle
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog takes orthomcl output (clusters) and produces an input
        file for the tool cafe, which performes max-likelihood reconstruction
        of ancestral states'''
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-o', '--orthomcl', dest = 'clusters',
    help = 'Orthomcl clusters', metavar='FILE',
    default = '')
cloptions.add_option('-f', '--fasta', dest = 'fasta',
    help = 'Fasta file containing sequences of Proteins', metavar='FILE',
    default = '')
cloptions.add_option('-s', '--species', dest = 'species',
    help = 'Protein to species mapping', metavar='FILE',
    default = '')
cloptions.add_option('-d', '--hmmout', dest = 'hmmout',
    help = 'Hmmout, containing domain annotated proteins', metavar='FILE',
    default = '')
cloptions.add_option('-p', '--pickle', dest = 'pickle',
    help = 'Filename for the pickled clusters', metavar='FILE',
    default = 'pickled_orthomcl_clusters.p')
(options, args) = cloptions.parse_args()
#==============================================================================
def species_list(f_species):
    species = SpeciesMapping()
    species.load(f_species)
    return list(species.all())
#==============================================================================
def main():
    cafe = Cafe()
    clusters = pickle.load(open(options.pickle,"r"))
    species = species_list(options.species)
    cafe.write(clusters,species)

if __name__ == '__main__':
    main()

