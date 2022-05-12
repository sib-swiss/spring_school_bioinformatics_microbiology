# Solution Step 2: Comparative Metagenome Analysis with SIAMCAT

General note: this guide has been written assuming you use a R.

---

## Download the taxonomic profiles and metadata


Look at the metadata, how many controls (`CTR`) and cases (`CRC` for colorectal cancer) are there?

<details>
<summary markdown="span">Solution</summary>

Load the data:
```r
load(url("https://zenodo.org/record/6524317/files/motus_profiles_study1.Rdata"))
```

We can check what there is in the metadata with:
```r
head(meta_study1)
```

There are many columns, but the one we are interesed in is "Group":
```r
table(meta_study1$Group)
```
Which results in:
```
CRC CTR 
 46  60 
```

There are 46 profiles from diseased patients (CRC) and 60 profiles from healthy individuals.

We can check if there is an overall trend in the profiles looking at a PCA plot:
```r
rel_ab = prop.table(motus_study1)
log_rel_ab = log10(rel_ab+ 10^-4)

# remove zero rows
log_rel_ab = log_rel_ab[rowSums(rel_ab) > 0,]

pc <- prcomp(t(log_rel_ab),
             center = TRUE,
             scale. = TRUE)

df = data.frame(
  pc1 = pc$x[,1],
  pc2 = pc$x[,2],
  Group = as.factor(meta_study1[rownames(pc$x),"Group"])
)

ggplot(df,aes(x = pc1,y = pc2, col = Group)) + geom_point()
```

<img src="https://raw.githubusercontent.com/sib-swiss/spring_school_bioinformatics_microbiology/master/docs/assets/images/Project3/step_2_pca.png" width="500">


Overall there is not a big shift visible from the PCA.

</details> 



## Identify which species show an association to colorectal cancer patients


- Try to apply a t-test or a Wilcoxon test to your data.

    <details>
    <summary markdown="span">Solution</summary>
    
    Since we observed before that the data is not normally distributed, we can use a Wilcoxon test instead of a t-test. We can test all microbial species for statistically significant differences. In order to do so, we perform a Wilcoxon test on each individual bacterial species.
    ```r
    # use the same log transformed data as before
    rel_ab = prop.table(motus_study1,2)
    log_rel_ab = log10(rel_ab+ 10^-4)
    
    # remove zero rows
    log_rel_ab = log_rel_ab[rowSums(rel_ab) > 0,]
    
    # we go through each measured species
    p.vals <- rep_len(1, nrow(log_rel_ab))
    names(p.vals) <- rownames(log_rel_ab)
    
    for (i in rownames(log_rel_ab)){
      x <- log_rel_ab[i,]
      y <- meta_study1[colnames(log_rel_ab),]$Group
      t <- wilcox.test(x~y)
      p.vals[i] <- t$p.value
    }
    head(sort(p.vals))
    ```
    
    Result:
    
    ```r
                      Dialister pneumosintes [ref_mOTU_v3_03630] 
                                                    1.277337e-07 
     Fusobacterium nucleatum subsp. animalis [ref_mOTU_v3_01001] 
                                                    1.137605e-06 
               Olsenella sp. Marseille-P2300 [ref_mOTU_v3_10001] 
                                                    2.184340e-05 
    Fusobacterium nucleatum subsp. vincentii [ref_mOTU_v3_01002] 
                                                    5.576030e-05 
              Anaerotignum lactatifermentans [ref_mOTU_v3_02190] 
                                                    8.752588e-05 
    Fusobacterium nucleatum subsp. nucleatum [ref_mOTU_v3_01003] 
                                                    1.667614e-04 
    ```
    
    The species with the most significant effect seems to be *Dialister pneumosintes*, so let us take a look at the distribution of this species:
    
    ```r
    species <- 'Dialister pneumosintes [ref_mOTU_v3_03630]'
    df.plot <- data.frame(
      log_rel_ab = log_rel_ab[species,],
      group = meta_study1[colnames(log_rel_ab),]$Group
    )
    
    ggplot(df.plot, aes(x=group, y=log_rel_ab)) +
      geom_boxplot(outlier.shape = NA) +
      geom_jitter(width = 0.08) + 
      xlab('') + 
      ylab('D. pneumosintes rel. ab. (log 10)')
    ```
    
    <img src="https://raw.githubusercontent.com/sib-swiss/spring_school_bioinformatics_microbiology/master/docs/assets/images/Project3/step2_wilc_test_1.png" width="500">
    
    </details> 
 


- Try to run SIAMCAT to do association testing.
    <details>
    <summary markdown="span">Solution</summary>
    
    We can also use the SIAMCAT R package to test for differential abundance and produce standard visualizations.
    ```r
    library("SIAMCAT")
    ```
    Within SIAMCAT, the data are stored in the SIAMCAT object which contains the feature matrix, the metadata, and information about the groups you want to compare.
    
    ```r
    rel_ab = prop.table(motus_study1,2)
    sc.obj <- siamcat(feat=rel_ab, meta=meta_study1, 
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
    label()                Label object:         60 CTR and 46 CRC samples
    filt_feat()            Filtered features:    1167 features after abundance, prevalence filtering
    
    contains phyloseq-class experiment-level object @phyloseq:
    phyloseq@otu_table()   OTU Table:            [ 33571 taxa and 106 samples ]
    phyloseq@sam_data()    Sample Data:          [ 106 samples by 12 sample variables ]
    ```
    
    We go from 33,571 taxa to 1,167 after abundance and prevalence filtering.
              
    Now, we can test the filtered feature for differential abundance with SIAMCAT:
    ```r
    sc.obj <- check.associations(sc.obj, detect.lim = 1e-05)
    ```
    
    <img src="https://raw.githubusercontent.com/sib-swiss/spring_school_bioinformatics_microbiology/master/docs/assets/images/Project3/step_2_association_testing_1.png">
    
    
    </details> 





