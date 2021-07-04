# ContFree-NGS.py

A very simple filter, open source software that removes sequences from contaminating organisms in your NGS dataset based on a previous taxonomic classification.

## Requirements
* python >= 3.8.5
* ETE Toolkit >= 3.1.2
* biopython >= 1.78

## Installation

### Get ContFree-NGS from GitHub
```bash
cd ~
git clone https://github.com/labbces/ContFree-NGS.git 
```

### Python dependencies 

Install ETE Toolkit (ete3):
```bash
pip install ete3
```

Install Biopython:
```bash
pip install biopython
```
## Usage



## Example 

We have prepared a Sugarcane contaminated dataset for your first run, it is available at `ContFree-NGS/data`. This dataset contains three files:
* `contaminated_sugarcane_1.fastq` and `contaminated_sugarcane_2.fastq`: Two paired-end files containing 1000 reads (800 from SP80-3280, a genotype of Sugarcane spp., 150 from the bacteria Acinetobacter baumanii and 50 from the fungus Aspergillus fumigatus);
* `contaminated_sugarcane.kraken`: A file with the NCBI Taxonomic ID for all of these reads. 

Check `ContFreeNGS/data/README.md` for more information about the Sugarcane contaminated dataset.

### Running ContFree-NGS in the contaminated dataset, keeping only taxons descendants of Viridiplantae  
```bash
./ContFree-NGS.py --taxonomy data/contaminated_sugarcane.kraken --left data/contaminated_sugarcane_1.fastq --right data/contaminated_sugarcane_2.fastq --taxon Viridiplantae 
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
* contaminated_sugarcane_1.filtered.fastq
* contaminated_sugarcane_1.unclassified.fastq
* contaminated_sugarcane_2.filtered.fastq
* contaminated_sugarcane_2.unclassified.fastq
