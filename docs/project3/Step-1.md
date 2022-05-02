# Step 1: Taxonomic profiling of metagenomic samples with mOTUs

General note: this guide has been written assuming you use a Mac or Linux Command Line.

---

## Download example sequencing data

During sequencing, the nucleotide bases in a DNA sample (library) are determined by the sequencer. For each fragment in the library, a sequence is generated, also called a read, which is simply a succession of nucleotides.
Sequencing data produced by a short read sequencer like Illumina HiSeq result in two fastq files: forwards and reverse. You can download three example fastq files at the following links (within a terminal):

```bash
wget https://www.embl.de/download/zeller/TEMP/NCCR_course/sampleA_1.fastq
wget https://www.embl.de/download/zeller/TEMP/NCCR_course/sampleA_2.fastq

wget https://www.embl.de/download/zeller/TEMP/NCCR_course/sampleB_1.fastq
wget https://www.embl.de/download/zeller/TEMP/NCCR_course/sampleB_2.fastq

wget https://www.embl.de/download/zeller/TEMP/NCCR_course/sampleC_1.fastq
wget https://www.embl.de/download/zeller/TEMP/NCCR_course/sampleC_2.fastq
```


When we work with metagenomic data we usually have two fastq files produced by
the Illumina sequencer:
- a file containing the forward reads
- a file containing the reverse reads

Usually the prefix of the file name is the same, and we have `_1_` for the file
with forward reads and `_2_` for the file with reverse reads, example:
```
HYG3LBGXC_261_1_19s00-sample119s004346_1_sequence.fq.gz
HYG3LBGXC_261_1_19s00-sample119s004346_2_sequence.fq.gz
```

A fastq file contains 4 lines for each read, with the following information:
  
 1. A line starting with `@` and the read id
 2. The DNA sequence
 3. A line starting with `+` and sometimes the same information as in line 1
 4. A string of characters that represents the quality score (same number of characters as in line 2)

We can have a look at the first read (4 lines) with `head -n 4 raw_reads_1.fastq`:
```
@read98
CATCGACGACCTGGACGACCTGGACTTCATCGAGCGGGTGAAGATCCAGCAGAAGAACTGGATCGGCCGCTCCACCGGTGCCGAGGTCACCTTCAAGGCC
+
BBBFFFFFFFFFFBBFFFFIIFFFIIIIIIIIFBFIIFFFFFFFBBBFFFFBBFFFFFBBFFFBBBFBBBBFBBFBFFBBFFF0<B7BBFBB<BBFBBBF
```

Each character in the fourth line can be converted to a quality score ([Phred-33](https://support.illumina.com/help/BaseSpace_OLH_009008/Content/Source/Informatics/BS/QualityScoreEncoding_swBS.htm)) from 1 to 40:
```
     Character: !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHI
                |         |         |         |         |
 Quality score: 0........10........20........30........40 
```

And, for each quality score there is an associated probability for correctly calling a base:

| Quality Score | Probability of incorrect base call | Base call accuracy |
| ------ | ------ | ------ | 
| 10 | 1 in 10 | 90% |
| 20 | 1 in 100 | 99% |
| 30 | 1 in 1000 | 99.9% |
| 40 | 1 in 10,000 | 99.99% |




Explore the files, in particular you can check:

- How many reads there are per sample?
- What is the average length of the reads? Is there a difference between forward and reverse?
- Do you have the same read IDs in the forward and reverse file? 










## Check the quality of the sequencing data

Modern sequencing technologies can generate a massive number of sequence reads in a single experiment. However, no sequencing technology is perfect, and each instrument will generate different types and amount of errors, such as incorrect nucleotides being called. These wrongly called bases are due to the technical limitations of each sequencing platform.

Therefore, it is necessary to understand, identify and exclude error-types that may impact the interpretation of downstream analysis. Sequence quality control is therefore an essential first step in your analysis. Catching errors early saves time later on.

You can evaluate the quality of fastq files with fastQC. For example run:

```bash
fastqc raw_reads_forward.fastq
```

Which will produce an html file. You can find more information on the different panels here: [link](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/)

- Which part of the reads is of lower quality?
- Is there any difference between forward or reverse?





## Filter and trim reads

The quality drops in the end of the sequences we analysed. This could cause bias in downstream analyses with these potentially incorrectly called nucleotides. Sequences must be treated to reduce bias in downstream analysis. Trimming can help to increase the number of reads the aligner or assembler are able to succesfully use, reducing the number of reads that are unmapped or unassembled. In general, quality treatments include:

1. Trimming/cutting: 
   - from low quality score regions
   - beginning/end of sequence
   - removing adapters
2. Filtering of sequences
   - with low mean quality score
   - too short
   - with too many ambiguous (N) bases

To accomplish this task we will use [trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic), a tool that enhances sequence quality by automating adapter trimming as well as quality control. Check [their website](http://www.usadellab.org/cms/?page=trimmomatic) to get more information on how to run the tool.

Note that if you installed trimmomatic with conda, you can run with `trimmomatic PE [...]` (do not need to specify `java -jar trimmomatic-0.39.jar PE [...]`).

- Try to run trimmomatic (you can use different parameters).
- How many files did trimmomatic generated? What do they contain?
- How many reads have been filtered out?
- Check the quality of the filtered reads, did the quality improve?








## Taxonomic profiling with mOTUs

The majority of microbiome studies rely on an accurate identification of the microbes and quantification their abundance in the sample under study, a process called taxonomic profiling.

We would like to save the profile in a file like:
```
Bacteroides_vulgatus    0.34
Prevotella_copri        0.16
Eubacterium_rectale     0.10
...
```

Where the first column contain the name of the species and the second column contain the relative abundance.

And, if we pull together many samples, in a table like:
```
                        sample_1  sample_2
Bacteroides_vulgatus        0.34      0.01
Prevotella_copri            0.16      0.42
Eubacterium_rectale         0.10      0.00
...                          ...       ...
```


We will use [mOTUs](https://github.com/motu-tool/mOTUs) to create taxonomic profiles of metagenomic samples.
More information can be found also in [this protocol paper](https://currentprotocols.onlinelibrary.wiley.com/doi/full/10.1002/cpz1.218).

- Use `motus` (manual: [link](https://github.com/motu-tool/mOTUs_v2#simple-examples)) to create a profile from the files created by trimmomatic.
- How many species are detected? How many are reference species and how many are unknown species?
- Can you change some parameters in `motus` to profile more or less species? (Hint, look [here](https://github.com/motu-tool/mOTUs/wiki/Increase-precision-or-recall))
- How can you merge different motus profiles into one file? Try to profile and then merge three profiles (Sample A, B and C).






## Taxonomic profiling with MAPseq

There are other taxonomic profiling tools that you can use, one that is already avaialble in the virtual machine is [MAPseq](https://github.com/jfmrod/MAPseq).

- Try to profile the three samples with MAPseq. (Note that MAPseq need fasta file as input, instead of fastq files)
- Files can be converted from fastq format to fasta in multiple ways. For our purpose with a small number of samples it is sufficiently fast to use sed to filter out the first and second lines of each read (4 lines in total). In order to convert your files, use the following command within your terminal:
```bash
sed -n '1~4s/^@/>/p;2~4p' sample.fastq > sample.fasta
```
- Similar as with mOTUs, first create a profile for each sample and then merge them into an otu-count table.
- Can you compare mOTUs and MAPseq profiles?








## Explore taxonomic profiles

Metagenomics enables the study of species abundances in complex mixtures of microorganisms and has become a standard methodology for the analysis of the human microbiome. However, species abundance data is inherently noisy and contains high levels of biological and technical variability as well as an excess of zeros due to non-detected species. This makes the statistical analysis challenging. Before moving to the next step, you will examine the properties of microbiome datasets.


We will switch now to R examine 496 human gut taxonomic profiles, from 124 patients (each measure 4 times over a period of 1 year). You can load the data within R with the command:
```R
load(url("https://www.embl.de/download/zeller/TEMP/NCCR_course/human_microbiome_dataset.Rdata"))
```

Explore the taxonomic profiles (`tax_profile`), here are some hints of what you can check:

- Which genera is the most and least prevalent?
- How many reads there are per sample?
- If you want to compare different samples, is it a problem that there are different read counts? Try to divide each value within a sample by the sum of the reads in that sample to normalise the data (also called relative abundance).
- Is the relative abundance of the different genera normally distributed?
- How many zeros there are per sample and per genus?
- How much variability there is within Subject (check the `metadata` table), compare to between subjects? Or from another perspective, how stable it is the human gut microbiome?
