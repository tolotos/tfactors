#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py



class SpeciesMapping:
	
	def __init__(self,protein):
		self.specmap = {}
		
    def load_organism(self, file):
        organisms = open(file, "r").readlines()
        for line in organisms:
            line = line.rstrip().split()
            name = line[0].replace(":","_")
            
            
            
            if self.proteins.has_key(name):
                self.proteins[name].species = line[1]
                if self.species_dic.has_key(line[1]):
                    pass
                else:
                    self.species_dic[line[1]] = 0

def main():
	
	return 0

if __name__ == '__main__':
	main()

