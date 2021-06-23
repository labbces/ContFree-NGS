#!/usr/bin/env python

'''						Description

'''

import argparse
import os
from ete3 import NCBITaxa
from Bio import SeqIO

# Creating arguments
parser = argparse.ArgumentParser(prog='ContFree-NGS.py', description='Removes contaminated sequences from Taxonomy Level in FASTQ files', add_help=True)
parser.add_argument('--taxonomy', dest='taxonomy_file', metavar='<taxonomy file>', help='A taxonomy classification file', required=True)
parser.add_argument('--left', dest='left_file', metavar='<left file>', help='left FASTQ file', required=True)
parser.add_argument('--right', dest='right_file', metavar='<left file>', help='right FASTQ file', required=True)
parser.add_argument('--level', dest='taxonomy_level', metavar='<Taxonomy level>', type=str, help='Only descendants from this Taxonomy Level will be maintained',required=True)
parser.add_argument('--v', '--version', action='version', version='%(prog)s v1.0')

#Getting arguments
args = parser.parse_args()
taxonomy_file = args.taxonomy_file
left_file = args.left_file
right_file = args.right_file
taxonomy_level = args.taxonomy_level

#checking indexed fastq files and create if it not exists	
def check_indexed_fastq_files():
	indexdb_left_file = left_file[:-5] + "index"
	indexdb_right_file = right_file[:-5] + "index"
	if not os.path.exists(indexdb_left_file) and not os.path.exists(indexdb_right_file):
		print("Indexing fastq files, please wait ...")
		left_index_db = SeqIO.index_db(indexdb_left_file, left_file, "fastq")
		right_index_db = SeqIO.index_db(indexdb_right_file, right_file, "fastq")

check_indexed_fastq_files()

#Opening fastq files indexdb
try:
	index_left = SeqIO.index_db(left_file[:-5] + "index")
	index_right = SeqIO.index_db(right_file[:-5] + "index")
except: 
	print("An exception occurred")

#Getting taxonomy database and taxonomy level
ncbi = NCBITaxa()
descendants = ncbi.get_descendant_taxa(taxonomy_level, intermediate_nodes=True)

#Getting user taxonomy level and append to descendants 
name2taxid = ncbi.get_name_translator([taxonomy_level])
the_values = name2taxid.values()  
user_tax_id = list(the_values)[0][0]
descendants.append(user_tax_id)

#Create output names
filtered_left = left_file[:-5] + "filtered.fastq"
filtered_right = right_file[:-5] + "filtered.fastq"
unfiltered_left = left_file[:-5] + "unclassified.fastq"
unfiltered_right = right_file[:-5] + "unclassified.fastq"

#Create counter
count_filtered_sequences = 0
count_unclassified_sequences = 0

#Filtering files
with open(taxonomy_file, "r") as taxonomy_classification_file, open(filtered_left, "w") as classified_left, open(filtered_right, "w") as classified_right, open(unfiltered_left, "w") as unclassified_left, open(unfiltered_right, "w") as unclassified_right:
	for line in taxonomy_classification_file:

		#Getting IDs
		left_sequence_id = line.split()[1] + "/1"
		right_sequence_id = line.split()[1] + "/2"
		taxonomy_id = int(line.split()[2])

		#Getting sequences in descendants (user taxonomic level)
		if line.startswith("C") and taxonomy_id in descendants:
			count_filtered_sequences += 1
			SeqIO.write(index_left[left_sequence_id], classified_left, "fastq")
			SeqIO.write(index_right[right_sequence_id], classified_right, "fastq")
		#Getting unclassified reads in taxonomy_classification_file file
		elif line.startswith("U"):
			count_unclassified_sequences += 1
			SeqIO.write(index_left[left_sequence_id], unclassified_left, "fastq")
			SeqIO.write(index_right[right_sequence_id], unclassified_right, "fastq")
	
	print("{} sequences are in the {} Taxonomic Level {}.".format(count_filtered_sequences, taxonomy_level))
	print("{} sequences was unclassified by the taxonomy classification file".format(count_unclassified_sequences))
	print("Filtered files was created as {} and {}".format(filtered_left, filtered_right))
	print("Unclassified files was created as {} and {}".format(unfiltered_left, unfiltered_right))