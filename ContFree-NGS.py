#!/usr/bin/env python

'''						Description
'''

import argparse
import os
from ete3 import NCBITaxa
from Bio import SeqIO

# Creating arguments
parser = argparse.ArgumentParser(prog='ContFree-NGS.py', description='Removing reads from contaminating organisms in Next Generation Sequencing datatasets', add_help=True)
parser.add_argument('--taxonomy', dest='taxonomy_file', metavar='<taxonomy file>', help='A taxonomy classification file', required=True)
parser.add_argument('--left', dest='left_file', metavar='<left file>', help='left read file', required=True)
parser.add_argument('--right', dest='right_file', metavar='<right file>', help='right read file', required=True)
parser.add_argument('--taxon', dest='taxon', metavar='<Taxon>', type=str, help='Only this taxon and its descendants will be maintained',required=True)
parser.add_argument('--v', '--version', action='version', version='%(prog)s v1.0')

#Getting arguments
args = parser.parse_args()
taxonomy_file = args.taxonomy_file
left_file = args.left_file
right_file = args.right_file
taxon = args.taxon

#Checking for indexed file and create it if dont exists	
def check_indexed_fastq_files():
	indexdb_left_file = left_file[:-5] + "index"
	indexdb_right_file = right_file[:-5] + "index"
	if not os.path.exists(indexdb_left_file) and not os.path.exists(indexdb_right_file):
		print("Indexing fastq files, please wait ... \n")
		left_index_db = SeqIO.index_db(indexdb_left_file, left_file, "fastq")
		right_index_db = SeqIO.index_db(indexdb_right_file, right_file, "fastq")

check_indexed_fastq_files()

#Opening indexed files
try:
	index_left = SeqIO.index_db(left_file[:-5] + "index")
	index_right = SeqIO.index_db(right_file[:-5] + "index")
except: 
	print("An exception occurred")

#Getting NCBI taxonomy database and user taxon
ncbi = NCBITaxa()
descendants = ncbi.get_descendant_taxa(taxon, intermediate_nodes=True)

#Translate user taxon and append it to descendants 
name2taxid = ncbi.get_name_translator([taxon])
the_values = name2taxid.values()  
user_tax_id = list(the_values)[0][0]
descendants.append(user_tax_id)

#Create output names
filtered_left = left_file[:-5] + "filtered.fastq"
filtered_right = right_file[:-5] + "filtered.fastq"
unfiltered_left = left_file[:-5] + "unclassified.fastq"
unfiltered_right = right_file[:-5] + "unclassified.fastq"

#Create counter
count_descendants_sequences = 0
count_unclassified_sequences = 0
count_contaminant_sequences = 0 
#Filtering files
with open(taxonomy_file, "r") as taxonomy_classification_file, open(filtered_left, "w") as classified_left, open(filtered_right, "w") as classified_right, open(unfiltered_left, "w") as unclassified_left, open(unfiltered_right, "w") as unclassified_right:
	for line in taxonomy_classification_file:

		#Getting IDs
		left_sequence_id = line.split()[1] + "/1"
		right_sequence_id = line.split()[1] + "/2"
		taxonomy_id = int(line.split()[2])

		#Getting sequences in descendants (user taxonomic level)
		if line.startswith("C"):
			if taxonomy_id in descendants:
				count_descendants_sequences += 1
				SeqIO.write(index_left[left_sequence_id], classified_left, "fastq")
				SeqIO.write(index_right[right_sequence_id], classified_right, "fastq")
			else:  
				count_contaminant_sequences += 1
		#Getting unclassified reads in taxonomy_classification_file file
		elif line.startswith("U"):
			count_unclassified_sequences += 1
			SeqIO.write(index_left[left_sequence_id], unclassified_left, "fastq")
			SeqIO.write(index_right[right_sequence_id], unclassified_right, "fastq")

	print("-------------------------------------------------")
	print("Contamination removal was successfully completed!")
	print("-------------------------------------------------")
	print("{} descendants sequences: {}".format(taxon, count_descendants_sequences))
	print("Contaminant sequences: {}".format(count_contaminant_sequences))
	print("Unlabelled sequences: {}".format(count_unclassified_sequences))
	print("-------------------------------------------------")
	print("{} descendants sequences are in the filtered files".format(taxon))
	print("Contaminant sequences were discarded")
	print("Unlabelled sequences are in the unclassified files")
