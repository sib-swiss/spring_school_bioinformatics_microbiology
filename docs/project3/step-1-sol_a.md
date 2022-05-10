
# Solutions Step 1: Taxonomic profiling of metagenomic samples with mOTUs

General note: this guide has been written assuming you use a Mac or Linux Command Line.

---

## Download example sequencing data


 Explore the files, in particular you can check:

  - How many reads there are per sample?
    <details>
    <summary markdown="span">Solution 1</summary>

    Knowing that each read takes up four lines in the fastq file, we can simply count the number of lines with `wc -l` and divide the result by `4`. The following command does it all in one line. 
    ```bash
    echo $(cat sampleA_1.fastq|wc -l)/4|bc
    ```
    </details> 
 
    <details>
    <summary markdown="span">Solution 2</summary>
     
    We can count the number of lines with `@read`:
    ```bash
    grep -c "@read" sampleA_1.fastq
    ```
 
    </details>

- What is the average length of the reads? Is there a difference between the read lengths in the forward and reverse files?
    <details>
    <summary markdown="span">Solution 1</summary>
 
    We can first extract only the sequences:
    ```bash
    grep -A 1 "@read" sampleA_1.fastq  | grep -v "\-\-" | grep -v "read" > sequences_sampleA_1
    ```
    With `-A 1` we select also 1 row after the match. With `grep -v` we remove what is not needed. We can now check the length with:
    ```bash
    cat sequences_sampleA_1 | awk '{print length}'
    ```
    This will print a big list, we can count how many times each length appear:
    ```bash
    cat sequences_sampleA_1 | awk '{print length}' | sort | uniq -c | sort -n | tail
    ```
    Which produces:
    ```bash
      238 96
      242 92
      258 93
      341 97
      344 94
      346 95   
      428 98
      849 20
     1194 99
    61306 100
    ```
    So the majority of the reads have length 100 (61,306 out of 67,926, 90%)
 
    </details>
    
    <details>
    <summary markdown="span">Solution 2</summary>
 
    To quickly check the average length of the reads in the terminal, do: 
    ```bash
    awk 'NR%4==2{sum+=length($0)}END{print sum/(NR/4)}' sampleA_1.fastq
    ```
    The average read length in the reverse reads seem to be slightly lower in all the samples.

    </details>

- Do you have the same read IDs in the forward and reverse file? 
    <details>
    <summary markdown="span">Solution</summary>

    Since these are paired reads, the read ids should be identical and in the same order. You can check this in the terminal like so: 

    ```bash
    #get list of read ids from the forward and reverse files
    grep '@read' sampleA_1.fastq > sampleA_ids_1.txt
    grep '@read' sampleA_2.fastq > sampleA_ids_2.txt
    #check if they are identical 
    diff -s sampleA_ids_1.txt  sampleA_ids_2.txt
    ```

    </details>

There are many different ways of performing the same task. If you have done something different and accomplished the same thing, awesome!


## Check the quality of the sequencing data

- Which part of the reads is of lower quality?
    <details>
    <summary markdown="span">Solution</summary>

    The ends of the reads are typically of lower quality. This is to be expected. The quality of calls typically degrades as the run progresses due to problems in the sequencing chemistry. 

    </details>
- Is there any difference between the quality of the forward and reverse reads?
    <details>
    <summary markdown="span">Solution</summary>

    Reverse reads are usually of lower quality than forward reads, particularly at the read ends. Again this is due to the way paired end sequencing is performed with the forward orientiation is sequenced first followed by the reverse orientation. 

    </details>


## Filter and trim reads

- Try to run trimmomatic (you can use different parameters).

    <details>
    <summary markdown="span">Solution</summary>
    
    Here is an example command: 

    ```bash
    trimmomatic PE sampleA_1.fastq sampleA_2.fastq sampleA_filtered_1P.fastq sampleA_filtered_1U.fastq sampleA_filtered_2P.fastq sampleA_filtered_2U.fastq ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
    ``` 
    Here is a description of the parameters used in this specific command. You may have explored other parameters too. 

    - `ILLUMINACLIP`: specifies the file containing the adapter sequences to trim and additional parameters on how to perform the adapter trimming. `TruSeq3-PE.fa` (provided by `trimmomatic`) contains the Illumina adapter sequences used by HiSeq and MiSeq machines. 
    - `LEADING`: Remove low quality bases (lower than `3`) from the beginning of the reads. 
    - `TRAILING`: Remove low quality bases (lower than `3`) from the ends of the reads.
    - `SLIDINGWINDOW`: consider a window of bases (here `4` at once) and trim once the average quality within the window falls below a threshold quality (here `15`). 
    - `MINLEN`: remove reads lower than the specified min length (here `36`)
    </details>


- How many files did trimmomatic generate? What do they contain?
    <details>
    <summary markdown="span">Solution</summary>
    
    4 files are produced

    - sampleA_filtered_1P, containing the forward reads that pass the filter and have a mate (in filtered_2P);
    - sampleA_filtered_1U, containing the forward reads that pass the filter and do not have a mate (the paired reverse read didn't pass the filter)
    - sampleA_filtered_2P, containing the reverse reads that pass the filter and have a mate (in filtered_1P);
    - sampleA_filtered_2U, containing the reverse reads that pass the filter and do not have a mate (the paired forward read didn't pass the filter)

    </details>
- How many reads have been filtered out?
    <details>
    <summary markdown="span">Solution</summary>
    
     866 reads (1.27%) of all reads were filtered out from sampleA using the above parameters. 

    </details>
 
- Check the quality of the filtered reads. Did the quality improve?
    <details>
    <summary markdown="span">Solution</summary>
     
     You can check the quality of the filterd reads again with fastqc. 

     ```
     fastqc sampleA_filtered_1P.fastq
     fastqc sampleA_filtered_2P.fastq
     ```
     The quality of reads (particularly of the reverse reads) has improved!
    </details>
 
## Taxonomic profiling with mOTUs

- Use `motus` (manual: [link](https://github.com/motu-tool/mOTUs_v2#simple-examples)) to create a profile from the files created by trimmomatic.
    <details>
    <summary markdown="span">Solution</summary>
     Here is the mOTU command to generate a taxonomic profile using default parameters.

     ```bash
     motus profile -f sampleA_filterd_1P.fastq -r sampleA_filtered_2P.fastq -s sampleA_filtered_1U.fastq,sampleA_filtered_2U.fastq -n sampleA -o sampleA_profile.txt
     ```

    </details>
- How many species are detected? How many are reference species and how many are unknown species?
    <details>
    <summary markdown="span">Solution</summary>
    You can quickly check how many species were detected with:

    ```bash
    #this also counts unassigned so subtract 1 from the result
    grep -c -v '0.0000000000\|#' sampleA_profile.txt
    ```
    `97` species were dectected. 
    Around `3.4 %` were unassigned . 

    You can check how many ref-mOTUs were detected using these command:
    ```bash
    grep -v '0.0000000000\|#' sampleA_profile.txt > sampleA_profile_detected.txt
    grep -c 'ref_mOTU_v3_' sampleA_profile_detected.txt
    ```
    `39` ref-mOTUs were detected in sampleA. Note that this number is also reported as stdout when you run `motus profile`

    </details>
  

- Can you change some parameters in `motus` to profile more or less species? (Hint, look [here](https://github.com/motu-tool/mOTUs/wiki/Increase-precision-or-recall))
        <details>
    <summary markdown="span">Solution</summary>
    Precision is the number of TP out of the total number of detected species. 

    Recall is the number of detected species out of all the species actually present in the sample. 

    To increase precision at the cost of recall you can increase parameters `-g` (default: 3) and -l (default: 75). 

    ```bash 
    motus profile -f sampleA_filterd_1P.fastq -r sampleA_filtered_2P.fastq -s sampleA_filtered_1U.fastq,sampleA_filtered_2U.fastq -n sampleA -o sampleA_profile_high_p.txt -g 8 -l 90
    ```
    We have detected just 37 species. 

    To increase recall at the cost of having more false positives you can do:

    ```bash 
    motus profile -f sampleA_filterd_1P.fastq -r sampleA_filtered_2P.fastq -s sampleA_filtered_1U.fastq,sampleA_filtered_2U.fastq -n sampleA -o sampleA_profile_high_r.txt -g 1 -l 45
    ```
    We have detected `331` species. 

    </details>



- How can you merge different motus profiles into one file? Try to profile and then merge three profiles (Sample A, B and C).

    <details>
    <summary markdown="span">Solution</summary>

    After creating the individual tax profiles for all the samples, do: 
    
    ```bash
    motus merge - i sampleA_profile.txt,sampleB_profile.txt,sampleC_profile.txt -o merged_profiles.txt
    ```
    This results in a tab-separated file containing the tax profiles. 
    </details>



## Taxonomic profiling with MAPseq

- Similar as with mOTUs, first create a profile for each sample (A,B, and C) and then merge them into one (Check the [github page](https://github.com/jfmrod/MAPseq) for the command). 

    <details>
    <summary markdown="span">Solution</summary>

    In order to create a taxonomic profile using `MAPseq` for sampleA do:

    ```bash
    mapseq sampleA_filtered_1P.fasta > sampleA.mseq
    ```
    `MAPseq` seems to be a bit faster than mOTUs (took ~2 min to run)

    `sampleA.mseq` contains the results from mapping reads to the reference database of OTUs provided by `MAPseq` (alignment score, database hit, etc) and the taxnomic classifications along with associated confidences. 

    After generating the `.mseq` files for all the samples, you can merge them into one OTU table like so:

    ```bash
    mapseq -otutable sampleA.mseq sampleB.mseq sampleC.mseq -ti 1 -tl 3 > mapseq_otutable_otu97.tsv
    ```
    This creates an OTU table containing reads mapped to 97% OTUs for sampleA, sampleB and sampleC. 

    Note that depending on whether `-ti` is 0 or 1, what `-tl` means changes. 

    If you have `-ti 0`, then `-tl` indicates the taxonomic level (0 (domain), 1 (phylum), 2 (class), 3 (order), 4 (family), 5 (genus), 6 (species)) . So if `-ti 0 -tl 3` means that the OTU table will report only read counts mapping to order-level NCBI taxonomies. 

    If you have `-ti 1`, then `-tl` indicates the OTU clustering level (1 (90% OTU), 2 (96% OTU), 3 (97% OTU), 4 (98%), 5 (99%)) . So if `-ti 1 -tl 3` means that the OTU table will report only read counts mapping to 97% OTUs. 

    To obtain reads mapping to 99% OTUs : 
    ```bash
    mapseq -otutable sampleA.mseq sampleB.mseq sampleC.mseq -ti 0 -tl 5 > mapseq_otutable_otu99.tsv
    ```

    If we increase the clustering level to 99%, we observe fewer species detected for all the samples. This might be because at a finer resolution, we might not be able to assign taxonomies too well resulting in a smaller number of species being profiled. 

    To obtain reads mapping to 96% OTUs : 

    ```bash
    mapseq -otutable sampleA.mseq sampleB.mseq sampleC.mseq -ti 0 -tl 2 > mapseq_otutable_otu96.tsv
    ```

    If we decrease the clustering level to 96%, we observe more species detected for all the samples. 

    </details>

- Can you compare mOTUs and MAPseq profiles?
    <details>
    <summary markdown="span">Solution</summary>

    | Profiler   | species detected in sampleA |
    |------------|-----------------------------|
    | mOTUs      | 97                          |
    | MAPseq 97% | 173                         |
    | MAPseq 99% | 121                         |
    | MAPseq 96% | 179                         |

    It looks like mOTUs is a bit more conservative at detecting species. Note that since mOTUs and OTUs are defined differently, it might not be straightforward to make a direct comparison. 
    </details>



