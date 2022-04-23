# Step 2: Comparative Metagenome Analysis with SIAMCAT

General note: this guide has been written assuming you use a R.

In R studio load the necessary libraries:
```R
library("tidyverse") # for general data wrangling and plotting
library("SIAMCAT")   # for statistical and machine learning analyses
```

---

## Download the taxonomic profiles and metadata

From the previous step you learned how to create taxonomic profiles. Here we provide 120 taxonomic profiles in the form of a table where columns are samples and rows are species (or clade in general). Within R you can download and load the files with the following command:

``` R
url_base = "https://www.embl.de/download/zeller/TEMP/NCCR_course/"

# mOTUs species table
feat.motus  <- paste0(url_base, 'Wirbel_species.motus')
tax.profiles <- read.table(feat.motus, sep = '\t', quote = '',
                           comment.char = '',
                           stringsAsFactors = FALSE, check.names = FALSE,
                           row.names = 1, header = TRUE)
tax.profiles <- as.matrix(tax.profiles)
```

Load the metadata with:
```R
meta.file  <- paste0(url_base, 'Wirbel.metadata')
meta <- read.table(meta.file,
                   sep = '\t', quote = '',
                   stringsAsFactors = FALSE, check.names = FALSE, 
                   row.names = 1, header = TRUE)
```


## Examine the profiles and the metadata

Look first at the taxonomic profiles and check how many zeros there are, what do they mean when you compare columns and rows zeros?

The values in the taxonomic profiles represent read counts, if you compare the different samples (columns), do you observe a similar total read count? Can it be a problem when comparing species counts across different samples?

Look at the metadata, how many control (`CTR`) and cases (`CRC` for colorectal cancer) are there?



## Identify which species show an association to colorectal cancer patients

How would you identify which species are associated to cancer? Which kind of test can you use?

Explore how SIAMCAT identify associations between clades and phenotypes: https://bioconductor.org/packages/release/bioc/vignettes/SIAMCAT/inst/doc/SIAMCAT_vignette.html


