#!/bin/bash
#SBATCH --job-name=cpu_notebook        #This is the name of your job
#SBATCH --cpus-per-task=48             #This is the number of cores reserved
#SBATCH --mem-per-cpu=4G               #This is the memory reserved per core.
#SBATCH --nodes=1                      # number of compute nodes
#SBATCH --time=6:00:00              #This is the time that your task will run
#SBATCH --qos=6hours                     #You will run in this queue

# Paths to STDOUT or STDERR files should be absolute or relative to current working directory
#SBATCH -o delta_export-%J.oe


# activate a conda environment of your choice (here we use base)
eval "$(conda shell.bash hook)"

conda activate delta2_env

export LD_LIBRARY_PATH="$CONDA_PREFIX/lib/"

## get tunneling info
XDG_RUNTIME_DIR=""
ipnport=$(shuf -i8000-9999 -n1)
ipnip=$(hostname -i)
pyvers=$(which python)

## print tunneling instructions to STDOUT
echo -e "
    Using Python: $pyvers

     Copy/Paste this in your local terminal to ssh tunnel with remote
-----------------------------------------------------------------
     ssh -N -L $ipnport:$ipnip:$ipnport vanvli0000@login.scicore.unibas.ch
-----------------------------------------------------------------

     Then open a browser on your local machine to the following address
------------------------------------------------------------------
     https://localhost:$ipnport  (see log file for token)
------------------------------------------------------------------
     "

## start an ipcluster instance and launch jupyter server
jupyter lab --no-browser --port=$ipnport --ip=$ipnip --keyfile=$HOME/.mycerts/mycert.key --certfile=$HOME/.mycerts/mycert.pem