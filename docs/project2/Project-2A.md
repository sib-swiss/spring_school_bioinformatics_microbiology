# Project 2A: Semi-automated processing using Fiji, Ilastik, and Python

Here we will use a semi-automated pipeline to segment time-lapse data and quantify cell properties over time. We will not track cells.

We will use a set of tools that are very frequently used in image analysis:

- [Fiji, aka: ImageJ on steroids](https://imagej.net/software/fiji/), which is a generalist user-friendly, GUI based, image analysis program offering many tools and plugins for manual and semi-automated analysis.
- [Ilastik](https://www.ilastik.org), which is a user-friendly, GUI based tool, offering several supervised machine learning pipelines.
- [python](https://neptune.ai/blog/image-processing-python), a generalist programming language which has become the language of choice for the image analysis community

General note: this guide has been written assuming you use a Mac or Linux Command Line.
For windows Powershell see [here](https://devblogs.microsoft.com/scripting/table-of-basic-powershell-commands/), for command prompt see [https://www.makeuseof.com/tag/essential-windows-cmd-commands/].

---

## Note on data

The dataset we will work with here consists of a time-lapse data of a synthetic microbial cross-feeding community consisting of two auxotrophic strains of *E. coli* that can only grow by exchanging Amino-Acids with each other. The two cell-types are fluorescently labeled with two different colors and grow together in a mono-layer within a 2D microfluidic growth chamber (a so-called family-machine).

---

## Create project folders

We first create a folder on your private computer for this course. Here we will assume it is `~/I2ICourse/` but you can use any folder (just change path variables accordingly).

- Open the command line and navigate to your home folder, then create a new folder called `I2ICourse` for the course:

```zsh
cd ~
mkdir I2ICourse
```

- Next create a folder for Project-2A `~/I2ICourse/Project2A/`:

```zsh
cd ~/I2ICourse/
mkdir Project2A
```

- And also make a folder for the processed data (output from all steps below):

```zsh
cd Project2A
mkdir ProcessedData
```

- This should have created the following folder: `~/I2ICourse/Project2A/ProcessedData/`:

- Note: two useful terminal commands are:
  - `ls`: show current folder content
  - `pwd`: show path of current folder

---

## Download Data

Here we will download the data via the command line.

- Navigate to the data folder:

```zsh
cd ~/I2ICourse/Project2A/
```

- Download the data set and unzip it using:
  
```zsh
wget -O RawData.zip https://drive.switch.ch/index.php/s/VsWWiuaIctITWQl/download
unzip RawData.zip
```

- You should now have a folder `~/I2ICourse/Project2A/RawData` containing 3 tif files (hint: use `ls` to check!)
- We can delete the zip-file using: `rm RawData.zip`

### Alternative Download via browser

If you have trouble downloading via command line, you can also use your browser:

- Open this [link](https://drive.switch.ch/index.php/s/VsWWiuaIctITWQl)
- Click Download
- Unzip the compressed file inside your data folder.
  - The data should now be located in `~/I2ICourse/Project2A/RawData`
  - Please rename the folder if needed

---

## Data preprocessing with Fiji

We will first prepare the data in Fiji

### Merging & splitting color channels

Before pre-processing we need to merge the color channels.

- Open the individual color images (`pos0-[c].tif`, where c={r,g,p})
- `Image` -> `Color` -> `Merge Channels`
- Make sure `Create composite` is selected
- Under C1 (red) select the [r] image
- Under C2 (green) select the [g] image
- Under C4 (grey) select the [p] image

- Save on disk as `pos0-merged.tif`
  - use your processed data folder, e.g.: `~/I2ICourse/Project2A/ProcessedData/`

### Crop Image

- Make a rectangular selection around the area of interest
- Make sure that you make the area big enough to accommodate any remaining jitter.
- Go to `Image`->`Crop`
- Save image as `pos0-preproc-merged.tif`
  - use your processed data folder, e.g.: `~/I2ICourse/Project2A/ProcessedData/`

### Export data for segmentation

First we split the image into separate color channels

- `Image` -> `Color` -> `Split Channels`
- Save the separate image channels under the name `pos0-preproc-[c].tif`

In addition we need a combined image with the red and green channels.

- Use `Merge Channels` to combine the red and green channels (do not include phase!).
- Save on disk as `pos0-preproc-rg.tif`
  - use your processed data folder, e.g.: `~/I2ICourse/Project2A/ProcessedData/`

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

Most important steps (see also the pdf in the Project2A repository folder):

- Open Ilastik
- Select `Pixel Classification` workflow
- Save it in processed data folder as 'proj2A-ilastik'
- Go to `Input Data`
  - Load the data of the red-green channel.
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
  - Select as output folder `~/I2ICourse/Project2A/ProcessedData/`

The output should be stored under the name `[input_file_name]_Probabilities.h5`, i.e. `pos0_preproc-rg_Probabilities.h5`.

---

## Post-process with Python

### Export Data on local computer

For the next steps we will switch to the cloud computers, but before that we need to transfer the data-file we just created:

- On your local computer, compress the `~/I2ICourse/Project2A/ProcessedData` folder into a zip-file
- Upload this zip file to a cloud drive
- Create a public share link and copy the address

### Setup project folders on cloud computer

- Login to the **cloud computer** (your tutor will provide info in how to do this)
- Launch the command window and create a `Project2A` folder within the `~\workdir\` folder:

```bash
cd ~/workdir/
mkdir Project2C
```

**Important Note: on the cloud computer we need to store all data in the `~/workdir/` folder or sub-folders of this, to make sure that files remain available after restarting the instance.**

Also add a `ProcessedData` subfolder to the `Project2A` folder:

```bash
cd Project2A
mkdir ProcessedData
```

### Download data on cloud computer

Now we download the data file we just uploaded to the cloud:

```bash
cd ~/workdir/Project2A/ProcessedData
wget -O data.zip public_link_to_your_zip_file
unzip -j data.zip
```

- Check that the data transferred successfully (use `ls`)
- If so, then you can remove the zip file use `rm data.zip`

### Download project code on cloud computer

- Navigate to the `workdir` folder and use the `git clone` command to download the course code:

```zsh
cd ~/workdir/
git clone https://github.com/sib-swiss/spring_school_bioinformatics_microbiology.git
```

- This will create the folder `~/workdir/spring_school_bioinformatics_microbiology/` which contains all the Jupyter notebooks as well as the other course files

### Launch Jupyter Labs

- Next  navigate to the project folder, activate the conda environment, and launch Jupyter Labs:

```zsh
cd ~/workdir/
conda activate i2i_env
jupyter lab
```

- In Jupyter Labs, navigate to `spring_school_bioinformatics_microbiology/projects/project2/Project2A/`
- Then open the `post_process_segementation.ipynb` notebook
- Now run the notebook, see here for [instructions on Jupyter Labs](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html) and follow the instructions in the notebook.