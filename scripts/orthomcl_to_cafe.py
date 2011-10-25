#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  orthomcl_to_cafe.py
#
#==============================================================================
from optparse import OptionParser
from Tfsuite.Parser.orthomcl import Orthomcl
from Tfsuite.Parser.hmmout import Hmmout
from Tfsuite.Parser.fasta import Fasta
from Tfsuite.Parser.species import SpeciesMapping
import os
import sys
import glob
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog takes orthomcl output (clusters) and produces an input
        input file for the tool cafe'''
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
        protein.add_cluster(orthomcl)
        protein.add_species(species)
    for cluster in orthomcl:
        cluster.add_proteins(hmmout)
        cluster.counts = species.all()
        cluster.add_counts()
    return orthomcl

def write_cafe(orthomcl,species):
    '''Writes a cafe input file. Species is a list, which contains all
       the species that should be included. Cafe needs this exact layout,
       therefore the \t and \n charcters are flushed directly.'''
    sys.stdout.write("FAMILYDESC"+"\t"+"FAMILY")
    for name in species:
        sys.stdout.write("\t"+name)
    for cluster in orthomcl:
        sys.stdout.write("\n"+"---"+"\t"+str(cluster.name))
        for name in species:
            sys.stdout.write("\t"+str(cluster.counts[name]))

#==============================================================================


def main():
    clusters = create_clusters(options.clusters,
                               options.hmmout,
                               options.fasta,
                               options.species)
    write_cafe(clusters,["homsa"])



if __name__ == '__main__':
    main()

