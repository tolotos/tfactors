#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  pickle_orthomcl_clusters.py

#==============================================================================
from optparse import OptionParser
from Tfsuite.Parser.orthomcl import Orthomcl
from Tfsuite.Parser.hmmout import Hmmout
from Tfsuite.Parser.fasta import Fasta
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
desc='''%prog takes orthomcl output (clusters) and creates a pickable object
        containing all loaded clusters.'''
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
def create_clusters(f_orthomcl,f_hmmout,f_fasta,f_species):
    ''' Loads an orthomcl output file, to create clusters. In addition proteins
        are added from the corresponding hmmout file, species information is
        added from speciesMapping(Andreas) and fasta sequences for each protein
        are loaded. Function returns an interable with cluster objects'''
    orthomcl, hmmout, fasta, species = Orthomcl(), Hmmout(), Fasta(), SpeciesMapping()
    fasta.load(f_fasta)
    hmmout.load(f_hmmout)
    orthomcl.load(f_orthomcl)
    species.load(f_species)
    for protein in hmmout:
        protein.add_sequence(fasta)
        protein.add_species(species)
    for cluster in orthomcl:
        cluster.add_proteins(hmmout)
        cluster.counts = copy.deepcopy(species.all())
        cluster.add_counts()
        cluster.add_cluster_to_members()
    return orthomcl

def main():
    clusters = create_clusters(options.clusters,
                               options.hmmout,
                               options.fasta,
                               options.species)
    pickle.dump(clusters, open(options.pickle, "wb"))

if __name__ == '__main__':
    main()

