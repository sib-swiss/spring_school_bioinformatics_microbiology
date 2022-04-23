# Using Delta on SciCore

## Access Scicore

- Access is via ssh: `ssh username@login.scicore.unibas.ch`
- To copy data use scp: `scp <options> source  destination`
  - Use the transfer nodes: `username@login-transfer.scicore.unibas.ch`
  - e.g. `scp file_in_active_path username@login-transfer.scicore.unibas.ch:home/folder_in_home_dir`

## Install miniconda

Download and install miniconda:

- `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
- `bash Miniconda3-latest-Linux-x86_64.sh`

Run  `conda init [shell_name]` where `shell_name` is the type of shell used by the cluster (e.g. `bash`, see instructions at end of installation step).

## Install delta environment

enter the following commands:

```bash
ml Java/11.0.3_7
conda create -n delta2_env cudnn=8 cudatoolkit=11 python=3.9 jupyterlab ipykernel
conda activate delta2_env
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib/"
pip install delta2
pip install elasticdeform
```

Note: this works on the A100 and RTX8000 partitions, for Pascal you will need `cudatoolkit=10`

## Using Jupyter

Please see [here](https://wiki.biozentrum.unibas.ch/pages/viewpage.action?pageId=100829566) for detailed instructions on how to do this.
In short:

- make sure the conda environment is setup and that the data has been copied
- prepare a bash script for the job (see the included  `GPUNotebook.sh`)
  - Adapt partition if needed, see [here](https://wiki.biozentrum.unibas.ch/display/scicore/4.+Queues+and+partitions)
  - Make sure to add the following lines:

```bash
ml Java/11.0.3_7
ml FFmpeg
eval "$(conda shell.bash hook)"
conda activate delta2_env
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib/"

jupyter lab [name_of_notebook]
```

- submit a job via sbatch. i.e. `sbatch GPUNotebook.sh`
- check if it has launched using `squeue -u [username]` (see [here](https://wiki.biozentrum.unibas.ch/display/scicore/10.+Monitoring) for details)
- When launched open the output file called `JupLab-[job-id].oe` e.g. using vim: `vim JupLab-[job-id].oe`
- Copy the ssh command to your **local** terminal
- Open your browser and open the website `https://localhost:[port_nr]/lab?token=[token_nr]`
  - See the output file for the port and token numbers
- You should now be connected to the Jupyter session on the cluster
- You can close vim using `esc` followed by `:q!`
- **Important:** kill your job when your are done using it: `scancel [jobid]` or `scancel -u [username]`
  - **warning:** `scancel -u [username]` kills all your jobs!

In case of problems: maybe you reconnected earlier on the same port. If so you can clear old sessions using `lsof -ti:[port_nr] | xargs kill -9` (run this on your local machine!)
