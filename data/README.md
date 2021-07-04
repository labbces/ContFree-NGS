## Contaminated Sugarcane dataset

We have prepared a Sugarcane contaminated dataset for yout first run. 

This dataset contains 1.000 paired-end reads in fastq format, which 800 reads come from `SP80-3280`, a genotype of Sugarcane spp. ([SRR1774134](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR1774134)), 150 reads come from the bacteria `Acinetobacter baumanii` ([SRR12763742](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR12763742)) and 50 reads come from the fungus `Aspergillus fumigatus` ([DRR289670](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=DRR289670)).

## Generating the contaminated Sugarcane dataset

To generate the contaminated Sugarcane dataset, we did the following steps: 

* Download of the reads above from the `Sequence Read Archive database`;
* Convert the reads from `.sra` to `fastq` using `sratoolkit`;
* Quality control of the reads, trimming reads with quality Q>20 and removing illumina adapters;
* Concatenate 800 reads from SP80-3280, 150 reads from Acinetobacter baumanii and 50 reads from Aspergillus fumigatus

## Taxonomic classification file

To assess the contamination of a NGS dataset, `ContFree-NGS` requires a taxonomic classification file. It can be generated with a taxonomic classification tool, such as Kraken2 (Wood et al., 2019), Kaiju (Menzel et al., 2016), CLARK (Ounit et al., 2015), Centrifuge (Kim et al., 2016) and others.

`ContFree-NGS` works with a taxonomic classification file that have the information of each sequence in a single line of output, like `Kraken2`'s standard output, a tab-delimited file with the following fields:

1. "C"/"U": a one letter code indicating that the sequence was either classified or unclassified.
2. The sequence ID, obtained from the FASTA/FASTQ header.
3. The taxonomy ID; this is 0 if the sequence is unclassified.

## Generating a taxonomic classification file for the contaminated Sugarcane dataset with Kraken2

First, we built a custom database containing the following reference libraries: `archaea`, `bacteria`, `viral`, `human`, `fungi`, `plant`, `protozoa` and the `NCBI non-redundant nucleotide database` with the following command:

```bash
kraken2-build --download-library archaea --db completeDB --no-masking --use-ftp
kraken2-build --download-library bacteria --db completeDB --no-masking --use-ftp
kraken2-build --download-library viral --db completeDB --no-masking --use-ftp
kraken2-build --download-library human --db completeDB --no-masking --use-ftp
kraken2-build --download-library fungi --db completeDB --no-masking --use-ftp
kraken2-build --download-library plant --db completeDB --no-masking --use-ftp
kraken2-build --download-library protozoa --db completeDB --no-masking --use-ftp
kraken2-build --download-library nt --db completeDB --no-masking --use-ftp
```

Then, we ran `Kraken2` to taxonomically classify the Sugarcane contaminated dataset:
```bash
kraken2 --db completeDB --report-zero-counts --confidence 0.05 --output sugarcane_contaminated.kraken --paired contaminated_sugarcane_1.fastq contaminated_sugarcane_1.fastq
```
Here we set --confidence as 0.05. A filtering threshold of 0.05 or 0.10 is indicated for general purposes by the authors, as mentioned in this [issue](https://github.com/DerrickWood/kraken2/issues/167). 
