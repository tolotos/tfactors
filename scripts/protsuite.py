#!/usr/bin/python

from ete2 import *
import os, glob, sys, copy, re




#============================================================================
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


