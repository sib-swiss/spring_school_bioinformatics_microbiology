# Project 0: Semi-automated processing using Fiji, Ilastik, and Python

General note: this guide has been written assuming you use a Mac or Linux Command Line.

---

## Create project folders

We first create a folder on your private computer for this course. Here we will assume it is `~/I2ICourse/` but you can use any folder (just change path variables accordingly).

- Open the command line and navigate to your home folder, then create a new folder called `I2ICourse` for the course:

```zsh
cd ~
mkdir I2ICourse
```

- Next create a folder for Project 0 `~/I2ICourse/Project0/`:

```zsh
cd ~/I2ICourse/
mkdir Project0
```

- And also make a folder for the processed data (output from all steps below):

```zsh
cd Project0
mkdir ProcessedData
```

- This should have created the following folder: `~/I2ICourse/Project0/ProcessedData/`:

- Note: two useful terminal commands are:
  - `ls`: show current folder content
  - `pwd`: show path of current folder

---

## Download Data

You have two options for downloading: via command line or via browser. Try via command line if you feel comfortable doing this, but if you get stuck just use the browser.

### Download via command line

Here we will download the data via the command line, you will need to do this if you e.g. work on a cluster.

- Navigate to the data folder:

```zsh
cd ~/I2ICourse/Project0/
```

- Download the data set and unzip it using:
  
```zsh
wget -O RawData.zip https://drive.switch.ch/index.php/s/YF5Jt6DiMpzzZ3C/download
unzip RawData.zip
```

- You should now have a folder `~/I2ICourse/Project0/RawData` containing 3 tif files (hint: use `ls` to check!)
- We can delete the zip-file using: `rm project0.zip`

### Download via browser

- Open this [link](https://drive.switch.ch/index.php/s/T5t9eczX7cb96FN)
- Click Download
- Unzip the compressed file inside your data folder.
  - The data should now be located in `~/I2ICourse/Project0/RawData`

---

## Data preprocessing with Fiji

We will first prepare the data in Fiji

### Merging & splitting color channels

Before pre-processing we need to merge the color channels.

- Open the individual color images (proj0-pos0-[c].tif, where c={r,g,p})
- `Image` -> `Color` -> `Merge Channels`
- Make sure `Create composite` is selected
- Under C1 (red) select the [r] image
- Under C2 (green) select the [g] image
- Under C4 (grey) select the [p] image

- Save on disk as proj0-pos0-merged.tif
  - use your processed data folder, e.g.: `~/I2ICourse/Project0/ProcessedData/`

### Crop Image

- Make a rectangular selection around the area of interest
- Make sure that you make the area big enough to accommodate any remaining jitter.
- Go to `Image`->`Crop`
- Save image as proj0-pos0-preproc-merged.tif
  - use your processed data folder, e.g.: `~/I2ICourse/Project0/ProcessedData/`

### Export data for segmentation

First we split the image into separate color channels

- `Image` -> `Color` -> `Split Channels`
- Save the separate image channels under the name proj0-pos0-preproc-[c].tif

In addition we need a combined image with the red and green channels.

- Use `Merge Channels` to combine the red and green channels (do not include phase!).
- Save on disk as proj0-pos0-preproc-rg.tif
  - use your processed data folder, e.g.: `~/I2ICourse/Project0/ProcessedData/`

---

## Aside: Other preprocessing steps

During preprocessing you would often also do some other steps, for example:

- Registration: i.e. aligning images between frames to compensate for stage and sample drift
- Deconvolution: i.e. correcting for diffraction artifacts to make segmentation easier.
  
Unfortunately we do not have time to go into this now, but please ask us during the breaks for more information!

---

## Segment with Ilastik

We will give a brief live-demo of how to use Ilastik, please let us know when you are at this step, so that we can get the entire group together.

You can find  detailed instructions (and a movie) [here](https://www.ilastik.org/documentation/pixelclassification/pixelclassification).

Most important steps:

- Open Ilastik
- Select `Pixel Classification` workflow
- Save it in processed data folder as 'proj0-ilastik'
- Go to `Input Data`
  - First load the data of the red-green channel.
  - If you have extra time, try repeat on the phase contrast channel instead  
  **Important: spend max 20 min on this step! we will not use this data further** 
  - **Important: when adding the input data, you might have to change the axis order: double click on the axis order (e.g. `zcyx`) and change to `tcyx`.**
- Go to `Feature Selection`
  - Select all features
- Go to `Training`
  - Make two labels: `Cells` and `BG`
  - Add sparse training points to indicate which pixels belong to cells and which to background
  - **Important: save your project frequently! Ilastik can crash!**
  - Use `Live Update` to visualize training
  - Evaluate the result by checking `Segmentation (Layer 1)`
  - You can use the `Uncertainty` to see where more training points need to be added
  - Focus attention on pixels in between cells
  - Once the segmentation looks good, check a few other frames and update training as needed, until it looks good for all frames.
- Go to `Prediction Export`
  - See details [here](https://www.ilastik.org/documentation/basics/export.html)
  - In `Export Settings` select `Probabilities` in the `source` field.
  - Open `Choose Export Image Setting` and select `hdf5` format.
  - Then click `Export All`
  - Select as output folder `~/I2ICourse/Project0/ProcessedData/`

The output should be stored under the name `[input_file_name]_Probabilities.h5`, i.e. `proj0_pos0_preproc-rg_Probabilities.h5`.

---

## Post-process with Python

We will switch to the cloud computers for this step.

- On the cloud computer, we have to recreate the project folder:

```zsh
cd ~
mkdir I2ICourse
```

- Then we have to transfer the data from your local computer to the cloud computer (ask tutors how to do this).

- Next  navigate to the project folder, activate the conda environment, and launch Jupyter Labs:

```zsh
cd ~/I2ICourse/
conda activate i2i_env
jupyter lab
```

- In Jupyter Labs, navigate to `Image2Insight/Project0_Ilastik/`
- Then open the `post_process_segementation.ipynb`
- Now run the notebook (see here for [instructions on Jupyter Labs](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html))