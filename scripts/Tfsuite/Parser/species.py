#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2011 f_zimm01 <f_zimm01@EBBICORE4>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       



   def load_species(self):
        mapping = {}
        organisms = open(self.organisms, "r").readlines()
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

