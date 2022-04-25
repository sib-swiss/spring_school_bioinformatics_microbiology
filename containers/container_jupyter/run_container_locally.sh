docker run \
--user root \
-e NB_UID=1000 \
-e NB_UMASK=002 \
-e JUPYTER_ENABLE_LAB=yes \
-e JUPYTER_TOKEN=test123 \
-p 8888:8888 \
geertvangeest/spring_school_bioinformatics_microbiology:jupyter \
start-notebook.sh
