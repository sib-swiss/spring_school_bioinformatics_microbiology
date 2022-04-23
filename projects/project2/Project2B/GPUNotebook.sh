#!/bin/bash
#SBATCH --job-name=JupLab
#SBATCH --time=06:00:00
#SBATCH --cpus-per-task=6
#SBATCH --mem=64G
#SBATCH --qos=6hours    # 30min, 6hours, 1day, 1week, infinite  --> 6hours default, slurm is backfilling so be specific with time
#SBATCH --partition=rtx8000  
#SBATCH --gres=gpu:1        # --gres=gpu:2 for two GPU, etc
#SBATCH -o JupLab-%J.oe

ml Java/11.0.3_7
ml FFmpeg

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