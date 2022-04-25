FROM tensorflow/tensorflow:2.9.0rc0-gpu-jupyter

RUN apt-get update && apt-get install -y \
    wget \
    libgl1-mesa-dev

RUN useradd --uid 1000 --user-group -m -s /bin/bash jupyter


ENV CONDA_DIR /opt/conda
RUN wget -O ~/miniconda.sh --quiet \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

USER 1000:1000
WORKDIR /home/jupyter

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

RUN conda init

# project2
ENV PART=project2
COPY ${PART}/environment.yml .
RUN conda env create \
-n ${PART} \
-f environment.yml

USER root
RUN chown -R 1000:1000 /opt/conda
RUN rm -r /tf/tensorflow-tutorials
USER 1000:1000
RUN conda install -y nb_conda_kernels


RUN rm environment.yml
