# Solution Step 2: Comparative Metagenome Analysis with SIAMCAT

General note: this guide has been written assuming you use a R.

---

## Download the taxonomic profiles and metadata


Look at the metadata, how many controls (`CTR`) and cases (`CRC` for colorectal cancer) are there?

<details>
<summary markdown="span">Solution</summary>

We can check what there is in the metadata with:
```r
head(meta)
```

There are many columns, but the one we are interesed in is "Group":
```r
table(meta$Group)
```
Which results in:
```
CRC CTR 
 60  60 
```

There are 60 profiles from diseased patients (CRC) and 60 profiles from healthy individuals.

We can check if there is an overall trend in the profiles looking at a PCA plot:
```r
rel_ab = prop.table(tax.profiles,2)
log_rel_ab = log10(rel_ab+ 10^-4)

# remove zero rows
log_rel_ab = log_rel_ab[rowSums(rel_ab) > 0,]

pc <- prcomp(t(log_rel_ab),
             center = TRUE,
             scale. = TRUE)

df = data.frame(
  pc1 = pc$x[,1],
  pc2 = pc$x[,2],
  Group = as.factor(meta[rownames(pc$x),"Group"])
)

ggplot(df,aes(x = pc1,y = pc2, col = Group)) + geom_point()
```

<img src="https://raw.githubusercontent.com/sib-swiss/spring_school_bioinformatics_microbiology/master/docs/assets/images/Project3/step_2_pca.png" width="500">

Overall there is not a big shift visible from the PCA.

</details> 



## Identify which species show an association to colorectal cancer patients

Colorectal carcinoma (CRC) is among the three most common cancers with more than 1.2 million new cases and about 600,000 deaths per year worldwide. If CRC is diagnosed early, when it is still localized, the 5-year survival rate is > 80%, but decreases to < 10% for late diagnosis of metastasized cancer. With the data that we just dowloaded, we can check if there is any association between specific bacterial species and CRC patients.

- How would you study and estimate these associations? How would you identify which species are associated to cancer? Which kind of test can you use?
- Try to apply a t-test or a Wilcoxon test to your data.

 <details>
 <summary markdown="span">Solution</summary>
 
 Since we observed before that the data is not normally distributed, we can use a Wilcoxon test instead of a t-test. We can test all microbial species for statistically significant differences. In order to do so, we perform a Wilcoxon test on each individual bacterial species.
 ```r
 # use the same log transformed data as before
 rel_ab = prop.table(tax.profiles,2)
 log_rel_ab = log10(rel_ab+ 10^-4)
 
 # remove zero rows
 log_rel_ab = log_rel_ab[rowSums(rel_ab) > 0,]
 
 # we go through each measured species
 p.vals <- rep_len(1, nrow(log_rel_ab))
 names(p.vals) <- rownames(log_rel_ab)
 
 for (i in rownames(log_rel_ab)){
   x <- log_rel_ab[i,]
   y <- meta[colnames(log_rel_ab),]$Group
   t <- wilcox.test(x~y)
   p.vals[i] <- t$p.value
 }
 head(sort(p.vals))
 ```
 
 Result:
 ```r
           Peptostreptococcus stomatis [ref_mOTU_v3_03281] 
                                              7.269695e-09 
                      Parvimonas micra [ref_mOTU_v3_04287] 
                                              2.888822e-08 
 Clostridiales species incertae sedis [meta_mOTU_v3_13876] 
                                              2.707524e-07 
                  Solobacterium moorei [ref_mOTU_v3_02442] 
                                              3.083312e-07 
                Dialister pneumosintes [ref_mOTU_v3_03630] 
                                              1.619592e-06 
 Porphyromonas species incertae sedis [meta_mOTU_v3_13569] 
                                              2.613795e-06 
 ```
 
 </details> 
 

- Explore how SIAMCAT identify associations between clades and phenotypes: [link](https://bioconductor.org/packages/release/bioc/vignettes/SIAMCAT/inst/doc/SIAMCAT_vignette.html)
- What kind of normalization SIAMCAT allow to use?
- Try to run SIAMCAT to do association testing.





## Build machine learning models to predict colorectal cancer patients from a metagenomic sample

Population-wide screening and prevention programs for colorectal cancer are recommended in many countries. Fecal occult blood testing (Hemoccult FOBT) is currently the standard noninvasive screening test. However, because FOBT has limited sensitivity and specificity for CRC and does not reliably detect precancerous lesions, there is an urgent demand for more accurate screening tests to identify patients who should undergo colonoscopy, which is considered the most effective diagnostic method. Here, we we can investigate the potential of fecal microbiota for noninvasive detection of colorectal cancer in several patients.

We can model the problem using machine learning.

- Explore the SIAMCAT basic vignette to understand how you can train machine learning models to predict colerectal cancer from metagenomic samples.



## Explore other profiling methods

We profiled the same samples with different methods.

Here you can load the mOTUs profiles at genus level (instead of species level):
``` R
feat.motus  <- "https://zenodo.org/record/6517497/files/study1_genus.motus"
tax.profiles.genus <- read.table(feat.motus, sep = '\t', quote = '',
                           comment.char = '', skip = 2,
                           stringsAsFactors = FALSE, check.names = FALSE,
                           row.names = 1, header = TRUE)
tax.profiles.genus <- as.matrix(tax.profiles.genus)
```

And here you can find the MAPseq profiles using 97% OTUs:
```R
feat.mapseq_97 = "https://zenodo.org/record/6517497/files/study1_97_otutable.mapseq"
mapseq.profiles97 <- read.table(feat.mapseq_97, sep = ',', quote = '',
                           comment.char = '',
                           stringsAsFactors = FALSE, check.names = FALSE,
                           row.names = 1, header = TRUE)
mapseq.profiles97 <- as.matrix(mapseq.profiles97)
```

Or 99% OTUs:
```R
feat.mapseq_99 = "https://zenodo.org/record/6517497/files/study1_99_otutable.mapseq"
mapseq.profiles99 <- read.table(feat.mapseq_99, sep = ',', quote = '',
                           comment.char = '',
                           stringsAsFactors = FALSE, check.names = FALSE,
                           row.names = 1, header = TRUE)
mapseq.profiles99 <- as.matrix(mapseq.profiles99)
```

- Do you see a similar signal using different taxonomic profiling tools or different taxonomic levels? 




## Prediction on External Data

We provide another dataset from a colorectal cancer 
metagenomic study. The study population was recruited in France, you can
find the data under:

```r
feat.motus_study2  <- "https://zenodo.org/record/6517497/files/study2_species.motus"
meta.file_study2  <- "https://zenodo.org/record/6517497/files/study2.metadata"
```

Note that the features are the same as the mOTUs species in study 1.

- Apply the trained model (from `study1_species.motus`) on this new dataset and check the model performance  on the external dataset. (**Tip**: Check out the help for the `make.prediction` function in `SIAMCAT`)
