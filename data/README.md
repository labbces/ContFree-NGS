## Artificially contaminated dataset for testing

We provide an artificially contaminated dataset for your first run! This dataset contains 1.000 paired-end reads in fastq format, which 800 reads come from `SP80-3280`, a genotype of Sugarcane spp. ([SRR1774134](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR1774134)), 150 reads come from the bacteria `Acinetobacter baumanii` ([SRR12763742](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR12763742)) and 50 reads come from the fungus `Aspergillus fumigatus` ([DRR289670](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=DRR289670)).

## Taxonomic classification file

To assess the contamination of a NGS dataset, `ContFree-NGS` requires a taxonomic classification file, a tab-delimited file with the following fields:

1. "C"/"U"      # One letter code indicating that the sequence was either Classified or Unclassified
2. Sequence ID  # Obtained from the FASTA/FASTQ header
3. Taxonomy ID  # NCBI Taxonomy ID for every sequence (0 if unclassified)

It can be generated with a taxonomy assignment engine, such as [Kraken2](https://github.com/DerrickWood/kraken2) (Wood et al., 2019), [Kaiju](https://github.com/bioinformatics-centre/kaiju) (Menzel et al., 2016), [Centrifuge](https://github.com/DaehwanKimLab/centrifuge) (Kim et al., 2016), [CLARK](http://clark.cs.ucr.edu/) (Ounit et al., 2015) and others.

`ContFree-NGS` exploits the taxonomic classification file that have the taxonomy ID for every sequence  taxonomic classification file that have the information of each sequence in a single line of output, like `Kraken2`'s standard output, 

## Generating a taxonomic classification file for the artificially contaminated dataset with Kraken2

To generate the taxonomic classification with Kraken2 you have to create a custom database containing reference libraries e.g. `archaea`, `bacteria`, `viral`, `human`, `fungi`, `plant`, `protozoa`, `NCBI non-redundant nucleotide database`. This can be done with the following command:

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

Then, build the database and ran `Kraken2` to taxonomically classify the artificially contaminated dataset:

```bash

kraken2 --build completeDB
kraken2 --db completeDB --report-zero-counts --confidence 0.05 --output sugarcane_contaminated.kraken --paired contaminated_sugarcane_1.fastq contaminated_sugarcane_2.fastq
```

NOTE: We set --confidence as 0.05. By the author of Kraken2, a filtering threshold of 0.05 or 0.10 is stated for general purposes as mentioned in this [issue](https://github.com/DerrickWood/kraken2/issues/167). 
