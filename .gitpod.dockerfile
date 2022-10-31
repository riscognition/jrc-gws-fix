FROM gitpod/workspace-full

RUN sudo add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable \
 && sudo apt-get update \
 && sudo apt-get install gdal-bin libgdal-dev