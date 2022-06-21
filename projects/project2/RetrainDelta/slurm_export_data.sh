#!/bin/bash

#SBATCH --job-name=export_data        #This is the name of your job
#SBATCH --cpus-per-task=4             #This is the number of cores reserved
#SBATCH --mem-per-cpu=4G              #This is the memory reserved per core.
#Total memory reserved: 16GB
#SBATCH --nodes=1                   # number of compute nodes


#SBATCH --time=7-00:00:00           #This is the time that your task will run
#SBATCH --qos=1week                 #You will run in this queue

# Paths to STDOUT or STDERR files should be absolute or relative to current working directory
#SBATCH --output=export_data_log                    #This is the joined STDOUT and STDERR file
#SBATCH --mail-type=END,FAIL,TIME_LIMIT
#SBATCH --mail-user=simon.vanvliet@unibas.ch        #You will be notified via email when your task ends or fails

#This job runs from the current working directory

#Remember:
#The variable $TMPDIR points to the local hard disks in the computing nodes.
#The variable $HOME points to your home directory.
#The variable $SLURM_JOBID stores the ID number of your job.

#load your required modules below
#################################
eval "$(conda shell.bash hook)"
conda activate delta2_env
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib/"

#export your required environment variables below
#################################################


#add your command lines below
#############################
cd $HOME / 
python mlsFig_mmTest.py
