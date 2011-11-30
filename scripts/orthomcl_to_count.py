#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  orthomcl_to_cafe.py
#
#==============================================================================
from optparse import OptionParser
from Tfsuite.Parser.species import SpeciesMapping
from Tfsuite.Parser.count import Count
import os
import glob
import copy
import cPickle as pickle
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog takes orthomcl output (clusters) and produces an input
        file for the tool count, which reconstructs the ancestral states using
        parsimony (dollo, or wagner)'''
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-s', '--species', dest = 'species',
    help = 'Protein to species mapping', metavar='FILE',
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
    count = Count()
    clusters = pickle.load(open(options.pickle,"r"))
    species = species_list(options.species)
    count.write(clusters,species)

if __name__ == '__main__':
    main()



