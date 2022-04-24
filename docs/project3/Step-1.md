# Step 1: Taxonomic profiling of metagenomic samples with mOTUs

General note: this guide has been written assuming you use a Mac or Linux Command Line.

---

## Download example fastq files

Sequencing data produced by a short read sequencer like Illumina result in two fastq files: forwards and reverse. You can download three example fastq files at the following links (within a terminal):
```bash
wget XY
```

## Check the quality of the sequencing data and filter out low quality reads

You can evaluate the quality of fastq files with fastQC. For example run:
```bash
fastqc raw_reads_forward.fastq
```

Which will produce an html file. You can find more information on the different panels here: [link](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/)

You can filter out low quality reads using trimmomatic. You can find more information [here](http://www.usadellab.org/cms/?page=trimmomatic).
Note that if you installed trimmomatic with conda, you can run with `trimmomatic PE [...]` (do not need to specify `java -jar trimmomatic-0.39.jar PE [...]`).

How many reads have been filtered out? After filtering the reads, check if the overall quality improve. 
