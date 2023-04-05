# syntax=docker/dockerfile:1
FROM python:3.11
ENV PYTHONUNBUFFERED=1
COPY . /phylobook_pipeline/

# Install Python stuff
WORKDIR /phylobook_pipeline
RUN pip install --upgrade pip
RUN pip install -r /phylobook_pipeline/requirements.txt

# Install phyml
WORKDIR /
RUN git clone https://github.com/stephaneguindon/phyml.git
WORKDIR /phyml/src

# Update some source files
RUN python /phylobook_pipeline/script/updatefiles.py

# make phyml
WORKDIR /phyml
RUN sh autogen.sh
RUN ./configure --enable-phyml 
RUN make

# Update location of phyml
# RUN sed -i 's/\/opt\/home\/wdeng\/phyml_v3.3.20220408/\/phyml/g' /phylobook_pipeline/script/paths.py
RUN mkdir -p /phylobook_pipeline/phyml/src
RUN cp /phyml/src/phyml /phylobook_pipeline/phyml/src/phyml
VOLUME /phylobook_pipeline/phyml/src

# Install Image-Magick
RUN apt-get -y update
RUN apt-get -y install imagemagick

# Overwrite /etc/ImageMagick-6/policy.xml
RUN mv /etc/ImageMagick-6/policy.xml /etc/ImageMagick-6/policy.xml.bak
RUN cp /phylobook_pipeline/policy.xml /etc/ImageMagick-6/policy.xml

# Install Java
RUN apt update
RUN apt -y install default-jre

WORKDIR /phylobook_pipeline
