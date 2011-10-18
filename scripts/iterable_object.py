#!/usr/bin/python


class Parse(object):
	
	def __init__(self, type, file):
		self.file = file
		self.type = type
				
	def load(self):
		if self.type == "fasta":
			return self.load_fasta()
		elif self.type == "hmmout":
			pass
		else:
			raise NameError("Unknown input file format")
			
	def load_fasta(self):
		fasta = Fasta()
		lines = open(self.file, "r").readlines()
		for line in lines:
			if line[0] == ">":
				name = line[1:].rstrip()
				fasta.seqs[name] = ""
			else:
				fasta.seqs[name] += line.rstrip()
		return fasta


class Fasta(Parse):

	def __init__(self):
		self.seqs = {}
	def __iter__(self):
		#We are an iterable, so return our iterator
		return self.forward()
	def forward(self):
		#The forward generator
		current_item = 0
		while (current_item < len(self.seqs)):
			current_item += 1
			yield self.seqs
			
			
	
def main():
	fasta = Parse("fasta","test.fa").load()
	for seq in fasta:
		print seq.values()
		
if __name__ == "__main__":
    main()
