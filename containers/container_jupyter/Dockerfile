FROM jupyter/minimal-notebook:lab-3.3.4

USER root
RUN cat /etc/skel/.bashrc >> /etc/bash.bashrc

RUN apt-get update

RUN apt-get install -y \
curl \
libhdf5-dev \
gcc \
g++ \
libtool \
openslide-tools	\
libvips-dev \
libgl1-mesa-dev

USER $NB_UID

# change back to notebook user
ENV CONDA=/opt/conda/bin

ENV PART=project1
COPY $PART/environment.yml .
RUN $CONDA/conda env create \
-n $PART \
-f environment.yml

ENV PART=project2
COPY $PART/environment.yml .
RUN $CONDA/conda env create \
-n $PART \
-f environment.yml

RUN ${CONDA}/conda install -y nb_conda_kernels

RUN rm -r /home/jovyan/work/
RUN rm environment.yml
