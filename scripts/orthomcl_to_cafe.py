#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  orthomcl_to_cafe.py

#=======================================================================
from optparse import OptionParser
from Tfsuite.Parser.orthomcl import Orthomcl
import os
#=======================================================================
#Command line options===================================================
#=======================================================================
usage = 'usage: %prog [options]'
desc="""%prog takes orthomcl output (clusters) and produces an input
		input file for the tool cafe"""
        
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-o', '--orthomcl', dest = 'file',
    help = 'Orthomcl clusters', metavar='FILE',
    default = '')
(options, args) = cloptions.parse_args()
#=======================================================================

def prot_to_spec(proteome):
    spec_dic = {}
    
    for name, protein in proteome.proteins.items():
        if spec_dic.has_key(protein.species):
            if spec_dic[protein.species].families.has_key(protein.family):
                spec_dic[protein.species].families[protein.family] +=1
        else:
            spec_dic[protein.species] = Species(protein.species)
            spec_dic[protein.species].import_families(proteome)
    return spec_dic
#============================================================================

#sys.stdout.write("FAMILYDESC"+"\t"+"FAMILY")
#for name, species in test.items():
#    sys.stdout.write("\t"+species.name)

#counts = []
#for name, species in test.items():
#    counts.append((zip(*species.families.items())[1]))
#    names = species.families.keys()

#counter = 0
#counts = zip(*counts)
#for name in names:
#    sys.stdout.write("\n"+"---"+"\t"+str(name))
#    for i in counts[counter]:
#        sys.stdout.write("\t"+str(i))
#    counter +=1



def main():
	orthomcl = Orthomcl()
	orthomcl.load(options.file)
	for i in orthomcl:
		print i.members

if __name__ == '__main__':
	main()
