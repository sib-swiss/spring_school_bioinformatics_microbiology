# Step 2: Comparative Metagenome Analysis with SIAMCAT

General note: this guide has been written assuming you use a R.

In R studio load the necessary libraries:
```R
library("tidyverse") # for general data wrangling and plotting
library("SIAMCAT")   # for statistical and machine learning analyses
```

---

## Download the taxonomic profiles and metadata

From the previous step you learned how to create taxonomic profiles. Within R you can load the files created with mOTUs with the following command:

``` R
feat.motus  <- "path/to/motus/merged/table"
tax.profiles <- read.table(feat.motus, sep = '\t', quote = '',
                           comment.char = '', skip = 2,
                           stringsAsFactors = FALSE, check.names = FALSE,
                           row.names = 1, header = TRUE)
```

Note that we use `skip = 2` tp skip the first two headers, and we skip `check.names` when loading in R because some mOTUs names are confusing for R (they are treated as comments).

Here we provide 106 human gut taxonomic profiles in the form of a table where columns are samples and rows are species (or clade in general). You can load it directly with:

```r
load(url("https://zenodo.org/record/6524317/files/motus_profiles_study1.Rdata"))
```

Look at the metadata, how many controls (`CTR`) and cases (`CRC` for colorectal cancer) are there?



## Identify which species show an association to colorectal cancer patients

Colorectal carcinoma (CRC) is among the three most common cancers with more than 1.2 million new cases and about 600,000 deaths per year worldwide. If CRC is diagnosed early, when it is still localized, the 5-year survival rate is > 80%, but decreases to < 10% for late diagnosis of metastasized cancer. With the data that we just dowloaded, we can check if there is any association between specific bacterial species and CRC patients.

- How would you study and estimate these associations? How would you identify which species are associated to cancer? Which kind of test can you use?
- Try to apply a t-test or a Wilcoxon test to your data.
- Explore how SIAMCAT identify associations between clades and phenotypes: [link](https://bioconductor.org/packages/release/bioc/vignettes/SIAMCAT/inst/doc/SIAMCAT_vignette.html)
- What kind of normalization SIAMCAT allow to use?
- Try to run SIAMCAT to do association testing.

The associations metrics computed by SIAMCAT are stored in the SIAMCAT
object and can be extracted by using `associations(sc.obj)`, if you want to
have a closer look at the results for yourself. For example, you can use it to plot a volcano plot of the
associations between cancer and controls using the output from SIAMCAT.





## Build machine learning models to predict colorectal cancer patients from a metagenomic sample

Population-wide screening and prevention programs for colorectal cancer are recommended in many countries. Fecal occult blood testing (Hemoccult FOBT) is currently the standard noninvasive screening test. However, because FOBT has limited sensitivity and specificity for CRC and does not reliably detect precancerous lesions, there is an urgent demand for more accurate screening tests to identify patients who should undergo colonoscopy, which is considered the most effective diagnostic method. Here, we we can investigate the potential of fecal microbiota for noninvasive detection of colorectal cancer in several patients.

We can model the problem using machine learning.

- Explore the SIAMCAT basic vignette to understand how you can train machine learning models to predict colerectal cancer from metagenomic samples.



## Explore other profiling methods

We profiled the same samples with MAPseq, you can load it with:

``` r
load(url("https://zenodo.org/record/6524317/files/mapseq_profiles_study1.Rdata"))
```

You can find two profile tables, one from 97% OTUs and one from 99% OTUs.

- Do you see a similar signal using different taxonomic profiling tools or different taxonomic levels? 




## Prediction on External Data

We provide another dataset from a colorectal cancer 
metagenomic study. The study population was recruited in Germany, you can
find the data under:

```r
load(url("https://zenodo.org/record/6524317/files/motus_profiles_study2.Rdata"))
```

Note that the features are the same as the mOTUs species in study 1.

- Apply the trained model (from `motus_profiles_study1.Rdata`) on this new dataset and check the model performance on the external dataset. (**Tip**: Check out the help for the `make.prediction` function in `SIAMCAT`, or the vignette).


We profiled this same dataset also with MAPseq, if you want to check it:

```r
load(url("https://zenodo.org/record/6524317/files/mapseq_profiles_study2.Rdata"))
```
