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
    
    The species with the most significant effect seems to be *Peptostreptococcus stomatis*, so let us take a look at the distribution of this species:
    
    ```r
    species <- 'Peptostreptococcus stomatis [ref_mOTU_v3_03281]'
    df.plot <- data.frame(
      log_rel_ab = log_rel_ab[species,],
      group = meta[colnames(log_rel_ab),]$Group
    )
    
    ggplot(df.plot, aes(x=group, y=log_rel_ab)) +
      geom_boxplot(outlier.shape = NA) +
      geom_jitter(width = 0.08) + 
      xlab('') + 
      ylab('P. stomatis rel. ab. (log 10)')
    ```
    
    <img src="https://raw.githubusercontent.com/sib-swiss/spring_school_bioinformatics_microbiology/master/docs/assets/images/Project3/step2_wilc_test_1.png" width="500">
    
    </details> 
 

- Explore how SIAMCAT identify associations between clades and phenotypes: [link](https://bioconductor.org/packages/release/bioc/vignettes/SIAMCAT/inst/doc/SIAMCAT_vignette.html)
- What kind of normalization SIAMCAT allow to use?
- Try to run SIAMCAT to do association testing.
    <details>
    <summary markdown="span">Solution</summary>
    
    We can also use the SIAMCAT R package to test for differential abundance and produce standard visualizations.
    ```r
    library("SIAMCAT")
    ```
    Within SIAMCAT, the data are stored in the SIAMCAT object which contains the feature matrix, the metadata, and information about the groups you want to compare.
    
    ```r
    rel_ab = prop.table(tax.profiles,2)
    sc.obj <- siamcat(feat=rel_ab, meta=meta, 
                      label='Group', case='CRC')
    ```
    
    We can use SIAMCAT for feature filtering as well. Currently, the matrix of taxonomic profiles contains 33,571 different bacterial species. Of those, not all will be relevant for our question, since some are present only in a handful of samples (low prevalence) or at extremely low abundance. Therefore, it can make sense to filter your taxonomic profiles before you begin the analysis. Here, we could for example use the maximum species abundance as a filtering criterion. All species that have a relative abundance of at least 1e-03 in at least one of the samples will be kept, the rest is filtered out.
    ```r
    sc.obj <- filter.features(sc.obj, filter.method = 'abundance', cutoff = 1e-03)
    ```
 
    Additionally we can filter based on the prevalence:
    ```r
    sc.obj <- filter.features(sc.obj, filter.method = 'prevalence', 
                              cutoff = 0.05, feature.type = 'filtered')
    ```
    
    And we can have a look at the object:
    ```r
    sc.obj
    ```
    Result:
    ```r
    siamcat-class object
    label()                Label object:         60 CTR and 60 CRC samples
    filt_feat()            Filtered features:    1095 features after abundance, prevalence filtering
    
    contains phyloseq-class experiment-level object @phyloseq:
    phyloseq@otu_table()   OTU Table:            [ 33571 taxa and 120 samples ]
    phyloseq@sam_data()    Sample Data:          [ 120 samples by 16 sample variables ]
    ```
    
    We go from 33,571 taxa to 1,095 after abundance, prevalence filtering.
              
    Now, we can test the filtered feature for differential abundance with SIAMCAT:
    ```r
    sc.obj <- check.associations(sc.obj, detect.lim = 1e-05)
    ```
    
    <img src="https://raw.githubusercontent.com/sib-swiss/spring_school_bioinformatics_microbiology/master/docs/assets/images/Project3/step_2_association_testing_1.png">
     
    You can look at the figure in more detail at [this link](https://raw.githubusercontent.com/sib-swiss/spring_school_bioinformatics_microbiology/master/docs/assets/images/Project3/step_2_association_testing_1.png).
    
    </details> 











## Build machine learning models to predict colorectal cancer patients from a metagenomic sample

Population-wide screening and prevention programs for colorectal cancer are recommended in many countries. Fecal occult blood testing (Hemoccult FOBT) is currently the standard noninvasive screening test. However, because FOBT has limited sensitivity and specificity for CRC and does not reliably detect precancerous lesions, there is an urgent demand for more accurate screening tests to identify patients who should undergo colonoscopy, which is considered the most effective diagnostic method. Here, we we can investigate the potential of fecal microbiota for noninvasive detection of colorectal cancer in several patients.

We can model the problem using machine learning.

- Explore the SIAMCAT basic vignette to understand how you can train machine learning models to predict colerectal cancer from metagenomic samples.

    The SIAMCAT machine learning workflow consists of several steps:
    
    <details>
    <summary markdown="span">Normalization</summary>
    SIAMCAT offers a few normalization approaches that can be useful for subsequent statistical modeling in the sense that they transform features in a way that can increase the accuracy of the resulting models. Importantly, these normalization techniques do not make use of any label information (patient status), and can thus be applied up front to the whole data set (and outside of the following cross validation).
    
    ```r
    sc.obj <- normalize.features(sc.obj, norm.method = 'log.std',
                                 norm.param = list(log.n0=1e-05, sd.min.q=0))
    # Features normalized successfully.
    sc.obj
    # siamcat-class object
    # label()                Label object:         60 CTR and 60 CRC samples
    # filt_feat()            Filtered features:    1095 features after abundance, prevalence filtering
    # associations()         Associations:         Results from association testing
    #                                              with 65 significant features at alpha 0.05
    # norm_feat()            Normalized features:  1095 features normalized using log.std
    # 
    # contains phyloseq-class experiment-level object @phyloseq:
    # phyloseq@otu_table()   OTU Table:            [ 33571 taxa and 120 samples ]
    # phyloseq@sam_data()    Sample Data:          [ 120 samples by 16 sample variables ]
    ```
    
    </details> 
    
    <details>
    <summary markdown="span">Cross Validation Split</summary>
    Cross validation is a technique to assess how well an ML model would generalize 
    to external data by partionining the dataset into training and test sets.
    Here, we split the dataset into 10 parts and then train a model on 9 of these
    parts and use the left-out part to test the model. The whole process is 
    repeated 10 times.
    
    ```r
    sc.obj <- create.data.split(sc.obj, num.folds = 10, num.resample = 10)
    # Features splitted for cross-validation successfully.
    ```
    </details> 
    
     
    </details> 
    
    
    <details>
    <summary markdown="span">Model Training</summary>
    
    Now, we can train a [LASSO logistic regression classifier](https://www.jstor.org/stable/2346178) in order to distinguish CRC cases and controls.

    ```r
    sc.obj <- train.model(sc.obj, method='lasso')
    # Trained lasso models successfully.
    ```
    </details>  
     
     
     
    </details> 
    
    <details>
    <summary markdown="span">Predictions</summary>
    This function will automatically apply the models trained in cross validation to their respective test sets and aggregate the predictions across the whole data set.


    ```r
    sc.obj <- make.predictions(sc.obj)
    # Made predictions successfully.
    ```
    </details> 
     
     
    </details> 
    
    <details>
    <summary markdown="span">Model Evaluation</summary>
    Calling the `evaluate.predictions` function will result in an assessment of precision and recall as well as in ROC analysis, both of which can be plotted:
    
    ```r
    sc.obj <- evaluate.predictions(sc.obj)
    # Evaluated predictions successfully.
    model.evaluation.plot(sc.obj)
    ```
    
    ROC:
    
    <img src="https://raw.githubusercontent.com/sib-swiss/spring_school_bioinformatics_microbiology/master/docs/assets/images/Project3/step_2_auc.png" width="500">
    
    Precision-recall:
    
    <img src="https://raw.githubusercontent.com/sib-swiss/spring_school_bioinformatics_microbiology/master/docs/assets/images/Project3/step_2_prec_rec.png" width="500">
    
    </details> 
     
   
    <details>
    <summary markdown="span">Model Interpretation</summary>
    
    Finally, the `model.interpretation.plot` function will plot characteristics of the models (i.e. model coefficients or feature importance) alongside the input data aiding in understanding how / why the model works (or not).

    
    ```r
    model.interpretation.plot(sc.obj, consens.thres = 0.7)
    ```
    
    <img src="https://raw.githubusercontent.com/sib-swiss/spring_school_bioinformatics_microbiology/master/docs/assets/images/Project3/step_2_ML_interpretation.png">
    
    </details> 
       
     
     
     
     
     
     
     
     
     
     
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
