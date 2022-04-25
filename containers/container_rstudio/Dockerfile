FROM rocker/rstudio:4.1.0

RUN sudo apt-get update && apt-get install -y \
libxt6 \
libgl1-mesa-glx \
libcurl4-openssl-dev \
libglpk-dev \
libxml2-dev \
libproj-dev \
libudunits2-dev \
libgdal-dev \
libgsl-dev \
libbz2-dev \
libclang-dev

USER rstudio

WORKDIR /home/rstudio

ENV CONDA=/home/rstudio/.local/share/r-miniconda/bin/

RUN R -e "install.packages('reticulate')"
RUN R -e "reticulate::install_miniconda()"
RUN $CONDA/conda init bash
COPY .profile /home/rstudio/
RUN mkdir /home/rstudio/workdir && chown 1000:1000 /home/rstudio/workdir

RUN $CONDA/conda config --set safety_checks disabled

ENV PART=project3
COPY $PART/R_requirements.R .
RUN Rscript R_requirements.R
COPY $PART/environment.yml .
RUN $CONDA/conda env create \
-n $PART \
-f environment.yml

USER root

RUN rm /home/rstudio/R_requirements.R && rm /home/rstudio/environment.yml
