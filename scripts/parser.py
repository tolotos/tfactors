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
	
    def load_tree(self):
	   self.tree = PhyloTree(self.tree, format=3)
 
   
    def load_fasta(self):
        sequences = open(self.fasta, "r").readlines()
        for line in sequences:
            if line[0] == ">":
                name = line[1:].rstrip()
                if name.find(":"):
                    name = name.replace(":","_")
            else:
                if self.proteins.has_key(name):
                    self.proteins[name].seq += line.rstrip()
                else:
                    pass

    def load_arrangement(self):
        arrag_dict = {}
        for name, protein in self.proteins.items():
                protein.collapse_domains()
        arrangement = open(self.arrangement, "r").readlines()
        for line in arrangement:
           line = line.split()
           arrag = "".join(line[0].split(";"))
           family = line[1]
           arrag_dict[arrag] = family
        for name, protein in self.proteins.items():
            prodom_string = "".join(protein.domains)
            if arrag_dict.has_key(prodom_string):
                protein.family = arrag_dict[prodom_string]
    
 
    
    def load_cluster(self, cluster_file):
        cluster_file = open(cluster_file, "r").readlines()
        for line in cluster_file:
            cluster_name = line.split("\t")[0].split("(")[0]
            members = line.rstrip().split()
            members = members[3:]
            for member in members:
                member = member.split("(")[0][6:]
                if self.clusters.has_key(cluster_name):
                    self.clusters[cluster_name].members.append(self.proteins[member])
                else:
                    self.clusters[cluster_name] = Cluster(cluster_name,self.proteins[member])
    
    def load_cafe(self,cafe_file):
        cafe_dic = {}
        cafe_file = open(cafe_file, "r").readlines()
        for line in cafe_file:
            if line[0] == "O":
                line = line.rstrip().split()
                #print line[3]#,line[2],line[3]
                cafe_dic[line[0]] = [line[1],line[2],line[3]]
        for name, cluster in self.clusters.items():
            cluster.tree = cafe_dic[cluster.name][0]
            cluster.p_value = float(cafe_dic[cluster.name][1])
            cluster.branch_p = cafe_dic[cluster.name][2]

