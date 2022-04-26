# Install software and packages

To get started quickly during the course, we ask you to prepare a few things before the start of the course.

We will use the following software:

- [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic)
- [fastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- [mOTUs](https://github.com/motu-tool/mOTUs)
- [MAPseq](https://github.com/jfmrod/MAPseq)
- [SIAMCAT](https://siamcat.embl.de/)

Please install these following the instructions below.  

---

## Install four tools using Miniconda

Conda is a package management system and environment management system that allow to quickly install, run and update packages and their dependencies. The first four tools can be easily installed using conda, we suggest to use [Miniconda](https://docs.conda.io/en/latest/miniconda.html). To install miniconda, follow the instructions  for [MacOS](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html), [Windows](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) or [Linux](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).

After installing miniconda, create a file named `NCCR_p3.yaml` with:

```bash
name: NCCR_p3
channels:
  - conda-forge
  - defaults
  - bioconda
dependencies:
  - python=3.8
  - fastqc=0.11.9
  - motus=3.0.1
  - trimmomatic=0.39
  - mapseq=1.2.6
```

In the terminal you can then type:

```bash
conda env create -f NCCR_p3.yaml
```

To create an environment with the four tools that we will run in the terminal. You need to activate the environment before using it:

```bash
source activate NCCR_p3
```

Note that mOTUs require around 7Gb of space and it will download 3.5 Gb when installing. Hence the installation can take a few minutes.



### Problems installing with conda

If you have problem installing the conda environment, it might be due to the size required for mOTUs. We suggest to remove motus and install it with `pip`.  First create a new yaml file (names `NCCR_p3_test2.yaml`):

```bash
name: NCCR_p3_test2
channels:
  - conda-forge
  - defaults
  - bioconda
dependencies:
  - python=3.8
  - fastqc=0.11.9
  - bwa
  - samtools
  - pip
  - trimmomatic=0.39
  - mapseq=1.2.6
```

Create and activate the environment:

```bash
conda env create -f NCCR_p3_test2.yaml
source activate NCCR_p3_test2
```

Install mOTUs with pip:

```bash
pip install motu-profiler
```

And download the database manually:

```bash
motus downloadDB
```


## Installing R packages

Within R (we suggest to use R studio), type:

```
##R Version 4.0.2 or above

#tidyverse packages for plotting and data wrangling
install.packages("tidyverse")

#SIAMCAT
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("SIAMCAT")
```
