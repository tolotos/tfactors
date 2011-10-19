#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       01_orthomcl.py

#=============================================================================
#Command line options=========================================================
#=============================================================================

usage = 'usage: %prog [options]'
desc="""%prog takes domain arrangment as subfamilies and maps them to sequences and species"""
        
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-f', '--arrangment2family', dest = 'arrangment2family',
    help = 'Required arrangement to family mapping', metavar='FILE',
    default = '/home/fabian/Dropbox/uni/Master/FM_1_TF/data/input/arrangement2family')
cloptions.add_option('-m', '--hmmout', dest = 'hmmout',
    help = 'Required hmmout file', metavar='FILE',
    default = '/home/fabian/Dropbox/uni/Master/FM_1_TF/data/input/TF.sequences.28092010.hmmout')
cloptions.add_option('-s', '--sequences', dest = 'sequences',
    help = 'Required fasta file containing all sequences', metavar='FILE',
    default = '/home/fabian/Dropbox/uni/Master/FM_1_TF/data/input/TF.sequences.28092010.fasta')
cloptions.add_option('-o', '--organisms', dest = 'organisms',
    help = 'Required mapping from sequence names to species', metavar='FILE',
    default = '/home/fabian/Dropbox/uni/Master/FM_1_TF/data/input/speciesMapping')    
(options, args) = cloptions.parse_args()

proteome = Proteome(hmmout, fasta, arrangement,organisms)

proteome.load_hmmout()
proteome.load_fasta()
proteome.load_arrangement()
proteome.load_species()
#proteome.load_cluster(clusters)

spec_dic = {}
for name, protein in proteome.proteins.items():
    if spec_dic.has_key(protein.species):
        spec_dic[protein.species].append(protein)
    else:
        spec_dic.setdefault(protein.species,[protein])
        

os.mkdir("species_fasta")
os.chdir("species_fasta")
for species, proteins in spec_dic.items():
    fasta_file = open(species + ".fa","w")
    for protein in proteins:
        fasta = protein.export_fasta()
        fasta_file.write(fasta[0])
        fasta_file.write(fasta[1].replace("*",""))
    fasta_file.close()
    
    
    

def main():
	
	return 0

if __name__ == '__main__':
	main()

