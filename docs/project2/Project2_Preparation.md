# Preparation before start of course

During the course we will use a number of software packages. To get started quickly during the course, we ask you to install a few of these before the start of the course.

In case you run into any problems please do not hesitate to contact Simon van Vliet (preferentially via Slack).

We will use the following software:

- Ilastik -> Please install before start of course following instructions below
- BACMMAN (Fiji-ImageJ) -> Please install before start of course following instructions below
- Python (Anaconda) -> No need to install, we will use cloud-based computers to run our Python code

For completeness we also include instructions on how to install Python/Anaconda on your own computers below, however you can ignore these for now.

---

## Ilastik

Ilastik is a flexible GUI based application that offers several machine learning based workflow for image analysis.
We will use it for supervised pixel segmentation.

- We will use Ilastik beta version 1.4.0b21 (or newer) in the course
- Download it [here](https://www.ilastik.org/download.html#beta)
- Expend the archive and move the Ilastik application to your application folder

---

## Bacmman

BACMMAN (BACteria in Mother Machine Analyzer) is a ImageJ plugin that offers a fully automated workflow to analyze mother machine data.

### Install Fiji

- Download [here](https://fiji.sc)
- On Mac/Linux: copy Fiji app to application folder (or other folder of choice)
  - Note: OSX will give a security warning, please go into settings to give permission to launch Fiji
- On Windows: copy Fiji app to a folder in your user space e.g. `C:\Users\[your name]\ImageJ.app`
  
### Already have Fiji installed?

Please install a fresh copy of Fiji nonetheless!  
You can have multiple copies of Fiji on your computer, simply rename the new copy of Fiji to e.g. Fiji_Bacmman.

### Update Fiji

- Start Fiji
- Update Fiji with default update sites (ImageJ / Fiji / Java 8):
  - Go to `Help` -> `Update`
  - In ImageJ Updater window click on `Apply Changes`
- Restart Fiji
- Repeat until message 'Your ImageJ is up to date!' message appears

### Install Bacmman

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

### Max OSX Only: Install terminal packages

Although Mac OSX has a number of Terminal packages included by default (e.g. git), other need to be installed manually. [Homebrew](https://docs.brew.sh/Installation#4) is a convenient package manager that allows you to obtain these packages. To install, follow these instructions:

- install OS X command line tools using: `xcode-select --install`
- Install [Homebrew](https://docs.brew.sh/Installation#4) package manager using: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
  - You will be asked for your admin password!
- Install wget using: `brew install wget`

---

## Optional: Download jupyter notebooks for course

**Note: during the course we will use cloud-based computers for this step, so you do not have to do this on your private machine.**

These instructions are provided for the sake of completeness in case you want to continue working on the project after the course.

- We need to obtain the code we need for the course by cloning the Git repository

- Open the command line and navigate to your home folder, then create a new folder called `I2ICourse` for the course:

```zsh
cd ~
mkdir I2ICourse
```

- Next navigate to this new folder and use the `git clone` command to download the course code:

```zsh
cd ~/I2ICourse/
git clone https://github.com/sib-swiss/spring_school_bioinformatics_microbiology.git
```

- This will create the folder `~/I2ICourse/spring_school_bioinformatics_microbiology/project2` which contains all the Jupyter notebooks as well as the other course files

---

## Optional: Install Conda (Python)

**Note: during the course we will use cloud-based computers for this step, so you do not have to do this on your private machine.**

These instructions are provided for the sake of completeness in case you want to continue working on the project after the course.

Note: all our code has been tested with Conda version 4.11 and python version 3.9

### Install Anaconda

- Important: if you have an older version of Anaconda installed (Anaconda2 or below) please first remove it and re-install the latest Anaconda3 version!

- Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) following the provided instruction.

- If you already have an Anaconda3 (or Mini Conda) installation, please update to latest version using:

```zsh
conda update conda
conda update --all
```

- Optionally: you can update to latest python version (3.9), but this is not needed (we will install python 3.9 in a virtual environment below). To update use:

```zsh
conda install python=3.9
```

Note: alternatively you can install MiniConda, this is a minimal conda install that takes up much less space than Anaconda, but provides identical functionality. Follow instructions [here](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/macos.html).

### Install Mamba

The conda package manager can be rather slow at times. Specifically it does not work well at all with one of the packages we will use.

Luckily there is a newer alternative to conda, called [mamba](https://mamba.readthedocs.io/en/latest/index.html). mamba and conda work interchangeably, and use same syntax: just replace `conda` with `mamba`. One exception: activating and deactivating environments has to be done with `conda`.

- Install mamba using

```zsh
conda install mamba -n base -c conda-forge
```

### Create new Conda Environment

- It is best practice to use a separate conda environment for each project, this way you avoid conflicts in package requirements.

- You can create a new conda environment with the following command:

```zsh
conda create --name [environment_name] [list of packages to install]
```

- Alternatively you can create a new environment from a `.yml` environment file that specifies all packages:

```zsh
conda env create -f environment.yml
```

- As mentioned above, conda can be slow to use, so if you installed `mamba` as described above you use this to create a new environment, by simply using `mamba env create ...`.

- We now create the environment for the course, using:

```zsh
mamba env create -f i2i_env.yml
```

---

## Optional: Test Conda environment

**Note: during the course we will use cloud-based computers for this step, so you do not have to do this on your private machine.**

These instructions are provided for the sake of completeness in case you want to continue working on the project after the course.

- First navigate to your project folder

```zsh
cd ~/I2ICourse/
```

- Then activate the conda environment:

```zsh
conda activate i2i_env
```

- Next open jupyter-labs:
  
```zsh
jupyter lab
```

- In Jupyter labs, navigate to `/I2ICourse/spring_school_bioinformatics_microbiology/project2/`
- Then open the `test_notebook.ipynb`
- Now run the notebook (see here for [instructions](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html))

---

## Notes

### Trouble-shooting

- In case of persistent problems, try deleting your existing Conda installation and install the latest version from link above.
  - Note: make sure to backup essential conda environments before doing this!

### Alternatives

You can use Jupyter Notebook instead of Jupyter Lab. Both have same functionality, but Jupyter Lab has a bit nicer interface.

- To install: replace `jupyterlab` with `notebook`
- To open: replace `jupyter-lab` with `jupyter notebook`

[Visual Studio Code (VS Code)](https://code.visualstudio.com) is a cross-platform app that you can use to run Jupyter Notebooks. It has some added advantage compared to Jupyter Notebook / Jupyter Lab: it has a nice and fully customizable interface, a great build-in debugger, and offers several useful extensions such as:

- Jupyter (required to Jupyter notebooks)
- Markdown All in One (Markdown support)
- Python
- Gitlens (full Git integration)
- Code Spell Checker (intelligent spell checking)
- and many others
