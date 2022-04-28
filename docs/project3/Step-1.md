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

Look at the fastq files, how are they structured?

<details><summary>Information about FastQ files</summary>
<p>


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

| Line | Description |
| ------ | ------ |
| 1 | A line starting with `@` and the read id |
| 2 | The DNA sequence | 
| 3 | A line starting with `+` and sometimes the same information as in line 1 | 
| 4 | A string of characters that represents the quality score (same number of characters as in line 2) | 

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


</p> 
</details>

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
- Check the quality of the filtered reads, did the quality improved?
