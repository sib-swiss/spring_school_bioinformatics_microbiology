# Step 2: Comparative Metagenome Analysis with SIAMCAT

General note: this guide has been written assuming you use a R.

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
