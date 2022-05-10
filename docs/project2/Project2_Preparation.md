# Preparation before start of course

To get started quickly during the course, we ask you to prepare a few things.

General note: this code has been developed for Linux / Mac and Windows users will have to make some modifications.
We will try to point them out below. You can also use [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) to run Linux on a Windows machine (you can run windows and linux side-by-side, no reboot required).


## Optional: Python Tutorial

For those with little or no Python experience: we recommend you have a look at the following two notebooks that very briefly introduced the most important concepts and syntax:

- [General python introduction](https://colab.research.google.com/github/Pseudomoaner/Homeworks_Incomplete/blob/main/ODE_Modelling/Introduction%20to%20Python.ipynb) (made available by [Oliver Meacock](https://github.com/Pseudomoaner), University of Lausanne)
- [Short intro to Pandas dataframes](https://colab.research.google.com/github/google/eng-edu/blob/main/ml/cc/exercises/pandas_dataframe_ultraquick_tutorial.ipynb) (made available by Google)

## Setup Cloud Drive

We will need to transfer data between our local computers and cloud workstations, for this you need access to a cloud drive (e.g. Dropbox, Google Drive, Switch Drive, etc.) with at least 3GB of free space. For those based at a Swiss institution: you can setup a free account at [SwitchDrive](https://www.switch.ch/drive/) which gives you 100GB of space.

## Install Software

During the course we will use a number of software packages, we ask you to install a few of these before the start of the course. In case you run into any problems please do not hesitate to contact Simon van Vliet (preferentially via Slack).
We will use the following software:

- Ilastik -> Please install before start of course following instructions [below](#ilastik)
- BACMMAN (Fiji-ImageJ) -> Please install before start of course following instructions [below](#bacmman)
- Python (Anaconda) -> No need to install, we will use cloud-based computers to run our Python code

For completeness we also include instructions on how to install Python/Anaconda on your own computers below, however you can ignore these for now.

---

## Installation Instructions

### Ilastik

Ilastik is a flexible GUI based application that offers several machine learning based workflow for image analysis.
We will use it for supervised pixel segmentation.

- We will use Ilastik beta version 1.4.0b21 (or newer) in the course
- Download it [here](https://www.ilastik.org/download.html#beta)
- Expand the archive and move the Ilastik application to your application folder

---

### Bacmman

BACMMAN (BACteria in Mother Machine Analyzer) is a ImageJ plugin that offers a fully automated workflow to analyze mother machine data.

#### Install Fiji

- Download [here](https://fiji.sc)
- On Mac/Linux: copy Fiji app to application folder (or other folder of choice)
  - Note: OSX will give a security warning, please go into settings to give permission to launch Fiji
- On Windows: copy Fiji app to a folder in your user space e.g. `C:\Users\[your name]\ImageJ.app`
  
#### Already have Fiji installed?

Please install a fresh copy of Fiji nonetheless!  
You can have multiple copies of Fiji on your computer, simply rename the new copy of Fiji to e.g. Fiji_Bacmman.

#### Update Fiji

- Start Fiji
- Update Fiji with default update sites (ImageJ / Fiji / Java 8):
  - Go to `Help` -> `Update`
  - In ImageJ Updater window click on `Apply Changes`
- Restart Fiji
- Repeat until message 'Your ImageJ is up to date!' message appears

#### Install Bacmman

- Go to `Help` -> `Update`
- In ImageJ Updater window  click on `Manage update sites`
- In the list select (add a tick to tick box) the following extra update sites:
  - BACMMAN (`https://sites.imagej.net/BACMMAN/`)
  - BACMMAN-DL (`https://sites.imagej.net/BACMMAN-DL/`)
  - ImageScience (`https://sites.imagej.net/ImageScience/`)
- Click `Close`
- In ImageJ Updater window click on `Apply Changes`
- Restart Fiji
  
---

### Optional: Install Mac OSX terminal packages

Although Mac OSX has a number of Terminal packages included by default (e.g. git), other need to be installed manually. [Homebrew](https://docs.brew.sh/Installation#4) is a convenient package manager that allows you to obtain these packages. To install, follow these instructions:

- install OS X command line tools using: `xcode-select --install`
- Install [Homebrew](https://docs.brew.sh/Installation#4) package manager using: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
  - You will be asked for your admin password!
- Install wget using: `brew install wget`

---

### Install Conda (Python)

Note: all our code has been tested with Conda version 4.11 and python version 3.9

- Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) or [Mini-conda](https://docs.conda.io/en/latest/miniconda.html) or [Mamba Forge](https://mamba.readthedocs.io/en/latest/installation.html) following the provided instruction.
- Mini-conda is a light weight version of Anaconda. Mamba is a faster, but fully compatible, alternative to conda.
- **Important**: if you have an older version of Anaconda installed (Anaconda2 or below) please first remove it and re-install the latest Anaconda3 version!
- If you already have an Anaconda3 (or Mini Conda) installation, please update to latest version using:

```bash
conda update conda
conda update --all
```

- Optionally: you can update to latest python version (3.9), but this is not needed (we will install python 3.9 in a virtual environment below). To update use:

```bash
conda install python=3.9
```

---

### Get project code and setup conda environment

Note: all our code has been tested with Conda version 4.11 and python version 3.9

#### Download code from github

- We need to obtain the code we need for the course by cloning the Git repository
- Open the command line and navigate to your home folder, then create a new folder called `I2ICourse` for the course:
- **Windows users**: if you don't have git, you can get it [here](https://git-scm.com/download/win)

```bash
cd ~
mkdir I2ICourse
```

- Next navigate to this new folder and use the `git clone` command to download the course code:

```bash
cd ~/I2ICourse/
git clone https://github.com/sib-swiss/spring_school_bioinformatics_microbiology.git
```

- This will create the folder `~/I2ICourse/spring_school_bioinformatics_microbiology/` which contains all the Jupyter notebooks as well as the other course files

#### Create Conda environment for project

- It is best practice to use a separate conda environment for each project, this way you avoid conflicts in package requirements.
- We now create the environment for the course, using the provided environment file, which you can find in `~/I2ICourse/spring_school_bioinformatics_microbiology/projects/project2/environment.yml`

**Important: Linux/Mac users use this command:**

```bash
cd ~/I2ICourse/spring_school_bioinformatics_microbiology/projects/project2/
conda env create -f environment.yml
```

**Important: Windows users use this command:**

(The Delta2 package is not available from conda for windows users, we will install it later by hand)

```bash
cd ~/I2ICourse/spring_school_bioinformatics_microbiology/projects/project2/
conda env create -f environment_windows.yml
```


#### Test Conda environment

- First navigate to your project folder

```bash
cd ~/I2ICourse/
```

- Then activate the conda environment:
  
```bash
conda activate i2i_env
```

- Next open jupyter-labs:
  
```bash
jupyter lab
```

- In Jupyter labs, navigate to `/I2ICourse/spring_school_bioinformatics_microbiology/projects/project2/`
- Then open the `test_notebook.ipynb`
- Now run the notebook (see here for [instructions](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html))

---

### Notes

#### Trouble-shooting

- In case of persistent problems, try deleting your existing Conda installation and install the latest version from link above.
  - Note: make sure to backup essential conda environments before doing this!

#### Alternatives

You can use **Jupyter Notebook** instead of Jupyter Lab. Both have same functionality, but Jupyter Lab has a bit nicer interface.

- To install: replace `jupyterlab` with `notebook`
- To open: replace `jupyter-lab` with `jupyter notebook`

Alternatively, [**Visual Studio Code (VS Code)**](https://code.visualstudio.com) is a cross-platform app that you can use to run Jupyter Notebooks. It has some added advantage compared to Jupyter Notebook / Jupyter Lab: it has a nice and fully customizable interface, a great build-in debugger, and offers several useful extensions such as:

- Jupyter (required to Jupyter notebooks)
- Markdown All in One (Markdown support)
- Python
- Gitlens (full Git integration)
- Code Spell Checker (intelligent spell checking)
- and many others

The conda package manager can be rather slow at times. Luckily there is a newer alternative to conda, called [**mamba**](https://mamba.readthedocs.io/en/latest/index.html). mamba and conda work interchangeably, and use same syntax: just replace `conda` with `mamba`.  
One exception: activating and deactivating environments still has to be done with the `conda` command.

- Install mamba using

```bash
conda install mamba -n base -c conda-forge
```
