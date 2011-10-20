class Fasta:

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
