# ContFree-NGS: Removing reads from contaminating organisms in Next Generation Sequencing data. 

We present ContFree-NGS, a very simple filter, open source software that removes sequences from contaminating organisms in your NGS datasets based on a previous taxonomic classification.

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
```
pip install ete3
```

Install Biopython:
```
pip install biopython
```

## Example 

We have prepared a Sugarcane contaminated dataset for your first run, available at ContFree-NGS/data. This dataset contains:
* 1000 paired-end reads (fastq format), which 80% come from SP80-3280, a genotype of Sugarcane spp. (SRR1774134), 15% from Acinetobacter baumanii (SRR12763742) and 5% from Aspergillus fumigatus (DRR289670)
* A file with the NCBI Taxonomic ID for all of these reads, generated with Kraken2, using the parameter --confidence 0.05.
 
### Running ContFree-NGS in a Sugarcane contaminated dataset, setting the Viridiplantae as the --taxon parameter  
```bash
./ContFree-NGS.py --taxonomy contaminated_sugarcane.kraken --left contaminated_sugarcane_1.fastq --right contaminated_sugarcane_2.fastq --taxon Viridiplantae 
```


