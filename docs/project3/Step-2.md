# Step 2: Comparative Metagenome Analysis with SIAMCAT

General note: this guide has been written assuming you use a R.

In R studio load the necessary libraries:
```R
library("tidyverse") # for general data wrangling and plotting
library("SIAMCAT")   # for statistical and machine learning analyses
```

---

## Download the taxonomic profiles and metadata

From the previous step you learned how to create taxonomic profiles. Here we provide 120 human gut taxonomic profiles in the form of a table where columns are samples and rows are species (or clade in general). Within R you can download and load the files with the following command:

``` R
# mOTUs species table
feat.motus  <- "https://zenodo.org/record/6517497/files/study1_species.motus"
tax.profiles <- read.table(feat.motus, sep = '\t', quote = '',
                           comment.char = '', skip = 2,
                           stringsAsFactors = FALSE, check.names = FALSE,
                           row.names = 1, header = TRUE)
tax.profiles <- as.matrix(tax.profiles)
```

Load the metadata with:
```R
meta.file  <- "https://zenodo.org/record/6517497/files/study1.metadata"
meta <- read.table(meta.file,
                   sep = '\t', quote = '',
                   stringsAsFactors = FALSE, check.names = FALSE, 
                   row.names = 1, header = TRUE)
```


Look at the metadata, how many controls (`CTR`) and cases (`CRC` for colorectal cancer) are there?



## Identify which species show an association to colorectal cancer patients

Colorectal carcinoma (CRC) is among the three most common cancers with more than 1.2 million new cases and about 600,000 deaths per year worldwide. If CRC is diagnosed early, when it is still localized, the 5-year survival rate is > 80%, but decreases to < 10% for late diagnosis of metastasized cancer. With the data that we just dowloaded, we can check if there is any association between specific bacterial species and CRC patients.

- How would you study and estimate these associations? How would you identify which species are associated to cancer? Which kind of test can you use?
- Try to apply a t-test or a Wilcoxon test to your data.
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
