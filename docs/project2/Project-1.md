# Segmentation and Tracking 2D Data with Delta2.0

[Delta 2.0](https://gitlab.com/dunloplab/delta) is a Deep Learning based workflow that can segment and track 1D (mother machine) and 2D (family machine and agar pads) data. It used to consecutive U-Net networks to first segment and then track cells. The pipeline is described in [this publication](https://doi.org/10.1371/journal.pcbi.1009797). Detailed instruction can be found [here](https://delta.readthedocs.io/en/latest/index.html)

## Install Delta

Delta is now available on conda-forge. Here we will create a new environment and install delta2 and ipykernel. Sometimes Conda can be a bit slow, and in the case of delta2 it might get stuck for a very long time.

Luckily there is a newer alternative to conda, called [mamba](https://mamba.readthedocs.io/en/latest/index.html). mamba and conda work interchangeably, and use the same syntax: just replace `conda` with `mamba`. One exception: activating and deactivating environments has to be done with `conda`. 

- First install mamba using `conda install mamba -n base -c conda-forge`
- Then we can use mamba to install delta2.0 using:
  
```zsh
mamba create --name i2i_p1_env -c conda-forge ipykernel delta2 pathlib matplotlib seaborn napari
```

- We can the activate the new environment using: `conda activate i2i_p1_env`
- Finally we use pip to install elastic-deform: 'pip install elasticdeform`

## Download test data

Run the `0_download_test_data_delta` notebook to get the test data (note this may take some time!)

## Run the pipeline

Work trough the `1_run_pipeline_delta` notebook to see how the Delta2 pipeline works.

Note: processing speeds on CPU are very slow (hours) so we won't be able to run the full analysis locally within the course.
We will illustrate how it works for a small s

## Analyze the results

Work trough the `2_post_processing_delta` notebook.
