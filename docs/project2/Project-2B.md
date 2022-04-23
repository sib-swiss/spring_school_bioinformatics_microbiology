# Segmentation and Tracking 2D Data with Delta2.0

[Delta 2.0](https://gitlab.com/dunloplab/delta) is a Deep Learning based workflow that can segment and track 1D (mother machine) and 2D (family machine and agar pads) data. It uses two consecutive U-Net networks to first segment and then track cells. The pipeline is described in [this publication](https://doi.org/10.1371/journal.pcbi.1009797). Detailed instruction can be found [here](https://delta.readthedocs.io/en/latest/index.html)

## Download test data

Run the `0_download_model_delta` notebook to download the pre-trained network and data (note this may take some time, best to run this over a break!)

## Run the pipeline

Work trough the `1_run_pipeline_delta` notebook to see how the Delta2 pipeline works.

Note: processing speeds on CPU are very slow so use a CUDA compatible GPU based computer whenever possible.

Note: we also provided some instructions on how to use Delta on the Scicore cluster of University Basel [see `scicore.md`], to use Delta on clusters of other institutions, please contact your local cluster managers.

You can also try-out Delta on [Google CoLabs](https://colab.research.google.com/drive/1UL9oXmcJFRBAm0BMQy_DMKg4VHYGgtxZ).

## Analyze the results

Work trough the `2_post_processing_delta` notebook.

## Analyze the data

Once you have the data analyzed, try to extract biological insight from it. Discuss with your tutor what question you could address. For this step on we encourage people to team-up in pairs/small-groups and work together. You can use the `3_expore_data_delta` notebook as a starting point.

## Note on data

The dataset we will work with consists of a time-lapse data of a micro-colony of *E. coli* cells growing on LB agar pads. Images were taken every 5min.

We have two channels: phase contrast and GFP. The GFP signal comes from a transcriptional reporter for Colicin Ib, a bacteriocin that is regulated by SOS-stress response.

More info on the data can be found [here](https://doi.org/10.1016/j.cels.2018.03.009).
