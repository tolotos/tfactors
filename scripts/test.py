#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       01_sequencetospecies.py
#===============================================================================
from Tfsuite.Parser.fasta import Fasta
from Tfsuite.Parser.hmmout import Hmmout

from optparse import OptionParser
#===============================================================================
#Command line options===========================================================
#===============================================================================
usage = 'usage: %prog [options]'
desc="""%prog takes domain arrangment as subfamilies and maps them to sequences and species"""
        
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-f', '--arrangment2family', dest = 'arrangment2family',
    help = 'Required arrangement to family mapping', metavar='FILE',
    default = '/home/fabian/Dropbox/uni/Master/FM_1_TF/data/input/arrangement2family')
cloptions.add_option('-m', '--hmmout', dest = 'hmmout',
    help = 'Required hmmout file', metavar='FILE',
    default = '/home/f_zimm01/Dropbox/uni/Master/FM_1_TF/data/input/TF.sequences.28092010.hmmout')
cloptions.add_option('-s', '--sequences', dest = 'sequences',
    help = 'Required fasta file containing all sequences', metavar='FILE',
    default = '/home/f_zimm01/Dropbox/uni/Master/FM_1_TF/data/input/TF.sequences.28092010.fasta')
cloptions.add_option('-o', '--organisms', dest = 'organisms',
    help = 'Required mapping from sequence names to species', metavar='FILE',
    default = '/home/fabian/Dropbox/uni/Master/FM_1_TF/data/input/speciesMapping')    
(options, args) = cloptions.parse_args()
#===============================================================================



def main():
	fasta, hmmout = Fasta(), Hmmout()
	fasta.load(options.sequences)
	hmmout.load(options.hmmout)
	
	for protein in hmmout:
		protein.add_sequence(fasta)
	
if __name__ == '__main__':
	main()

