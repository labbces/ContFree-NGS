# ContFree-NGS
![Status: Inactive](https://img.shields.io/badge/status-inactive-orange) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)


ContFree-NGS is a lightweight, open-source filtering tool designed to remove contaminant sequences from NGS datasets based on a taxonomic classification file (e.g., from Kraken or similar tools). It parses classification results and filters out reads assigned to undesired taxa.

>[!IMPORTANT]
>Thanks for your interest in ContFree-NGS! Please note that this tool is no longer actively maintained. I strongly recommend using [KrakenTools](https://github.com/jenniferlu717/KrakenTools) for comprehensive analysis of Kraken/Kraken2/Bracken outputs.

---

# requirements
* python >= 3.8.5
* ETE Toolkit >= 3.1.2
* biopython >= 1.78

---

# installation

```bash
# clone this repository
git clone https://github.com/labbces/ContFree-NGS.git 

# install python dependencies

# installing ETE Toolkit (ete3)
pip install ete3

# installing Biopython
pip install biopython
```

--- 

# usage

Opening the help page:

```
./ContFree-NGS.py -h

usage: ContFree-NGS.py [-h] --taxonomy <taxonomy file> --sequencing_type, --s <p or s> --R1 <R1 file> [--R2 <R2 file>] --taxon <Taxon> [--v]

Removing reads from contaminating organisms in Next Generation Sequencing datatasets

optional arguments:
  -h, --help            show this help message and exit
  --taxonomy <taxonomy file>
                        A taxonomy classification file
  --sequencing_type, --s <p or s>
                        paired-end (p) or single-end (s)
  --R1 <R1 file>        FASTQ file 1
  --R2 <R2 file>        FASTQ file 2
  --taxon <Taxon>       Only this taxon and its descendants will be maintained
  --v, --version        show program's version number and exit
```

There are four required parameters: 

`--taxonomy`: Taxonomy classification file (output of kraken2 or other classification tool).

`--sequencing_type`: Use 'p' for paired-end reads or 's' for single-end reads.

`--R1 and --R2`: For paired-end reads use --R1 for read file 1 and --R2 for read file 2. If you are working with single-end reads, use --R1 for read files. 

`--taxon`: The user must provide a target a taxon (e.g Viridiplantae), which only sequences labeled in this target taxon or its descendants will be maintained in the filtered file. Sequences that not belong to the target taxon will be discarded and sequences that were not labeled at any taxon will be kept in the unclassified file. 

ContFree-NGS will process the NGS dataset and its taxonomic classification file in the following way:

<img src="https://github.com/labbces/ContFree-NGS/blob/main/images/pipeline.png" width="500">

a) The user generates a taxonomic classification file and run ContFree-NGS providing a target taxon.

b) ContFree-NGS creates an indexed database for the NGS dataset to reduce processing time; 

c) Then, checks whether the labeled taxon for any sequence belongs to the target taxon or its descendants, generating filtered and unclassified files. 

Note that the accuracy of ContFree-NGS contamination removal is directly dependent on the accuracy of the taxonomic classification engine, as ContFree-NGS uses the taxonomic label of each sequence to remove those that are from contaminants.

---

# example 

To assess the contamination of a NGS dataset, ContFree-NGS exploits a taxonomic classification file containing a taxon ID (NCBI Taxonomic ID) for every sequence in the dataset. This taxonomic classification file can be generated with a taxonomic classification tool, such as [Kraken2](https://github.com/DerrickWood/kraken2) or [Kaiju](https://github.com/bioinformatics-centre/kaiju).

We have prepared a artificially contaminated dataset for your first run, it is available at [ContFree-NGS/data/](https://github.com/labbces/ContFree-NGS/tree/main/data). This dataset contains three files:
* [artificially_contaminated_1.fastq](https://github.com/labbces/ContFree-NGS/blob/main/data/artificially_contaminated_1.fastq) and [artificially_contaminated_2.fastq](https://github.com/labbces/ContFree-NGS/blob/main/data/artificially_contaminated_2.fastq): Two paired-end files containing 1000 reads (800 from SP80-3280, a genotype of Sugarcane spp., 150 from the bacteria Acinetobacter baumanii and 50 from the fungus Aspergillus fumigatus);
* [artificially_contaminated.kraken](https://github.com/labbces/ContFree-NGS/blob/main/data/artificially_contaminated.kraken): A file with the NCBI Taxonomic ID for all of these reads. 

Check [data](https://github.com/labbces/ContFree-NGS/tree/main/data) for more information about the artificially contaminated dataset.

---

# running ContFree-NGS in the contaminated dataset, keeping only taxons descendants of Viridiplantae  

```bash
./ContFree-NGS.py --taxonomy data/artificially_contaminated.kraken --s p --R1 data/artificially_contaminated_1.fastq --R2 data/artificially_contaminated_2.fastq --taxon Viridiplantae 
```

This should print the following in your screen:
```
Indexing fastq files, please wait ... 

-------------------------------------------------
Contamination removal was successfully completed!
-------------------------------------------------
Viridiplantae descendants sequences: 410
Contaminant sequences: 128
Unlabelled sequences: 462
-------------------------------------------------
Viridiplantae descendants sequences are in the filtered files
Contaminant sequences were discarded
Unlabelled sequences are in the unclassified files
```

And should generate the files: 
* artificially_contaminated_1.filtered.fastq
* artificially_contaminated_1.unclassified.fastq
* artificially_contaminated_2.filtered.fastq
* artificially_contaminated_2.unclassified.fastq

---

# runtime and RAM usage

ContFree-NGS runtime and RAM usage are described in the chart below:

![Runtime and RAM usage](/images/runtime_and_RAM_usage.png)

This figure shows the RAM usage and time consuming to remove contaminants for the three artificially contaminated datasets.

Reading and writing a file is an operation that takes considerable time. If you are working with big files, we recommend that you split the taxonomic classification file into smaller files. This can be done as follows:

```bash
split -l lines -d --additional-suffix=.taxonomic_file artificially_contaminated.kraken splitted_
```

This should split your large taxonomic classification file into small files with a determinated prefix (splitted_n), where 'n' is the number of small files.  

---

# contact

For questions, feel free to open an [issue](https://github.com/labbces/ContFree-NGS/issues).

---

# citation

Peres, F.V., Riaño-Pachón, D.M. (2021). ContFree-NGS: Removing Reads from Contaminating Organisms in Next Generation Sequencing Data. Advances in Bioinformatics and Computational Biology. BSB 2021. Lecture Notes in Computer Science, vol 13063. Springer, Cham. DOI: https://doi.org/10.1007/978-3-030-91814-9_6

---

# license 

```
MIT License

Copyright (c) 2025 Felipe Vaz Peres

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
