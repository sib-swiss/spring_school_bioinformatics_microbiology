# Segmentation and Tracking Mother Machine Data with Bacmman & DistNet

## Getting started

This tutorial has been adapted from [this Wiki](https://github.com/jeanollion/bacmman/wiki/DistNet) page of Jean Ollion by Simon van Vliet.

Bacmman is described extensively in this [Nature Protocols article](https://doi.org/10.1038/s41596-019-0216-9), however note that some parts are outdated. 

The Distnet Deep Learning network is described in [this publication](https://arxiv.org/abs/2003.07790).

## Create a Dataset

Important: If using bacmman for the first time: choose a working directory through right-click on the panel below `Working Directory`.

We will start by creating a dataset using the default template of BACMMAN:
Choose menu command: `Dataset > New Dataset from Online Library`.

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/1_new_ds.png)

Set `jeanollion` as `username` in the `Github Credentials` panel (if not already entered), and select the configuration `ExampleDatasets > dataset1_distnet`

**Important: select the data set with "_distnet" at the end (the image is incorrect)!**

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/2_select_ds.png)

Click `OK`: this will create a new dataset and open it.
In BACMMAN a dataset is a configuration associated to multi-position/multi-channel/muti-frame input images.
The configuration can be checked in the `Configuration` tab.

## Download Example Dataset and Import Images

A subset of 50 of the example dataset 1 can be downloaded directly from BACMMAN. To do so, choose menu command: `Import > Sample Datasets > Mother Machine > Phase Contrast`, and select the directory where it will be downloaded.

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/3_dl_sample_data.png)

Import the downloaded images into the open dataset, by choosing the menu command `Run > Import/re-link Images`:

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/4_import_image.png)

An element will appear in the `Position panel`.
To visualize the images right click-on the position and choose `Open Input Images`

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/4_open_ii.png)

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/4_inputimage.png)

## Run Pre-Processing

In this case pre-processing consist of an automatic rotation of the images to have microchannels vertically aligned with the open end towards the lower part of the image.
The images are also cropped to remove the bright line and useless area of the image.  

To run pre-processing

* Select the position (when no position is selected, all positions are processed)
* Select the task: `Pre-Processing` 
* Choose the menu command `Run > Run Selected Tasks`

**Important: only select `Pre-Processing` at this stage (the image is incorrect)!**

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/5_run_pp_mc.png)

To visualize the pre-processed images right-click on the position and choose `Open Pre-Processed Images`

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/5_open_pi.png)

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/5_pp_image.png)

### Download Model Weights

As DiSTNet is a deep-learning based method, it requires trained weights of the model.
To download them:

1. Go to the `Configuration Test` tab
2. In the `Step` pannel select `Processing`
3. Select the `Bacteria` object class : it's configuration will be displayed below
4. Unfold the parameters `Tracker` > `Model > Tensorflow Model`. The sub-parameter `Model File` appears in red if the model weights are not there. However it is possible to download them directly from BACMMAN.
5. Right-click on `Tensorflow Model` and choose `Download Model`. The model weights will be downloaded at the path selected in the `Model File` parameter, that should not appear in red anymore after the download.

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/7_model_weights_not_there.png)

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/7_dl_model.png)

## Run tracking and segmentation

* Go back to the `Home` tab
* Select the objects Microchannels and Bacteria at the same time
* Select the task: `Segmentation & Tracking`
* Choose the menu command `Run > Run Selected Tasks`

**Important: only select `Segmentation & Tracking` at this stage (the image below is incorrect)!**

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/5_run_pp_mc.png)

## Check micro-channel segmentation and tracking

To visualize the result of microchannel segmentation and tracking:

* Go to the `Data Browsing` tab
* Right-click on the position and choose `Open Hyperstack > Microchannels`

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/6_open_mc_hyperstack.png)

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/6_mc_hyperstack.png)

The pre-processed images will open as a interactive hyperstack (multi-channel & multi-frames image stack), on which microchannels can be selected.

* To display all segmented microchannels object use the shortcut `crtl + A`
* To display all microchannels tracks use the shortcut `crtl + Q`. Tracks will be displayed as colored contours, each colour corresponding to one track.
* Note that the shortcut are available from the menu `Help > Display Shortcut table` and that a shortcut preset adapted for QWERTY keyboards can be chosen from the menu `Help > Shortcut Presets`

## Check bacterial segmentation and tracking

To visualize the result of bacterial segmentation and tracking:

* Go to the `Data Browsing` tab
* Right-click on the position and choose `Open Hyperstack > Bacteria`

The pre-processed images will open as a interactive hyperstack (multi-channel & multi-frames image stack), on which bacteria can be selected.

* To display all segmented bacteria object use the shortcut `crtl + A`
* To display all bacteria tracks use the shortcut `crtl + Q`. Tracks will be displayed as colored contours, each colour corresponding to one track.
* Note that the shortcut are available from the menu `Help > Display Shortcut table` and that a shortcut preset adapted for QWERTY keyboards can be chosen from the menu `Help > Shortcut Presets`

Another good way to visualize tracking is to use the Kymograph view:

* In the `Segmentation & Tracking Results` area, click on the arrow next to `Position #0`  to expand the list of micro channels. 
* Right-click on a micro-channel and choose `Open Kymograph > Bacteria`
* The resulting image shows a concatenation of the same micro-channel for all time points  
* To display all segmented bacteria object use the shortcut `crtl + A`
* To display all bacteria tracks use the shortcut `crtl + Q`. Tracks will be displayed as colored lines connecting neighboring time points.

![](https://github.com/jeanollion/bacmman/wiki/resources/tuto_distnet/8_seg_track_results.png)

## Export the data

* Go to the `Home tab`
* Select the object `Bacteria` and the task `Extract Measurements`
* Choose the menu command `Run > Run Selected Tasks`

## Post-processing in Python

Setup a new conda environment:

- `conda create --name i2i_p2_env -c conda-forge python=3.9 ipykernel numpy scipy matplotlib scikit-image pandas napari seaborn`
- `conda activate i2i_p2_env`
- `pip install PyBacmman`

Now open notebook `0_making_selection` in the project 2 folder of the repository

