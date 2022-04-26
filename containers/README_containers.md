# How to use the containers

## General information

- During the course the containers are hosted on an AWS EC2 instance.
- Each student gets assigned one container of each available type (i.e. Rstudio, jupyter ..)
- Computational resources are limited per container. By default this is 16G RAM and 4 CPU. This can be increased if needed. The limits are hard, meaning that if they get exceeded (especially RAM), the container will crash and automatically restared (everything in working memory will be lost). 
- Each container will get a unique port assigned, so a link to an individual container will look like `123.34.455:10034`. 
- In the container, you can find the following shared directories:
    - `/data`: read only, and shared between all running containers. This directory is used to have a single place to store data
    - `/group_work`: read and write enabled for all participants, and shared between all containers. This can be used to share data/scripts between students. This directory can be backed up. 
    - `~/workdir`: read and write enabled, and only shared between containers assigned to the same participant. This directory can be backed up and shared as a tarball at the end of the course. 
- All directories other than the shared directories only exist within the container. 

## Hosting locally

- For testing, or doing the exercises outside the course, the containers can be run locally. 
- Example scripts to run them can be found in this repo at `containers/container_[tag]/run_container_locally.sh`. After running this script, you can login:
    - For `rstudio`: go to `localhost:8787` in your browser. Use the username `rstudio` and the password specified at `-e PASSWORD=` in the `docker run` command\
    - For `jupyter`: go to `localhost:8888` in your browswer. Use the password specified at `-e JUPYTER_TOKEN=` to log in. 

## Jupyter containers

- Interaction with the container is either via the terminal, jupyter notebook or python console. 
- Software of individual sessions (e.g. projects) will be in a conda environment. Check which environments are available with `conda env list`. You can use these environments in two ways:
    - Using the terminal, e.g. `conda activate env_name`
    - By switching the kernel of jupyter notebooks (e.g. by using **Kernel** > **Change Kernel..** )

## Rstudio containers

- All R packages will be installed in the system library. 
- Conda environments are installed with the `reticulate` conda installation. Check which environments are available with `conda env list`.
- You can use the conda environments in two ways:
    - Using the terminal, e.g. `conda activate env_name`
    - In `R` (with `reticulate`): `reticulate::use_condaenv("env_name")`. 
