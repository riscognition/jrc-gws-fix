FROM gitpod/workspace-full

RUN sudo add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable \
 && sudo apt-get -y update \
 && sudo apt-get -y install gdal-bin libgdal-dev