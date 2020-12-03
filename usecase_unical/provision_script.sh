#!/usr/bin/env bash
# Configure environment
export CONDA_DIR=/opt/conda
export PATH=$CONDA_DIR/bin:$PATH
export SHELL=/bin/bash
export DEBIAN_FRONTEND=noninteractive

# Install dependencies
apt-get update
apt-get install -yq --no-install-recommends \
git \
vim \
wget \
build-essential \
python-dev \
ca-certificates \
bzip2 \
unzip \
libsm6 \
pandoc \
texlive-latex-base \
texlive-latex-extra \
texlive-fonts-extra \
texlive-fonts-recommended \
openjdk-8-jre-headless

apt-get clean

# Install conda
mkdir -p $CONDA_DIR
echo export PATH=$CONDA_DIR/bin:'$PATH' > /etc/profile.d/conda.sh
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
/bin/bash Miniconda3-latest-Linux-x86_64.sh -f -b -p $CONDA_DIR
rm Miniconda3-latest-Linux-x86_64.sh
$CONDA_DIR/bin/conda install --yes conda==4.3.21


# Install Jupyter notebook
conda install --yes 'notebook=5.0*' terminado
conda clean -yt

#Create Jupyter working folders
mkdir /root/work
mkdir /root/.jupyter
mkdir /root/.local

# Spark dependencies
export APACHE_SPARK_VERSION=2.1.1
apt-get -y update
apt-get install -y --no-install-recommends openjdk-7-jre-headless
apt-get clean
echo 'Downloading Spark. Hold tight..'
wget -qO - http://d3kbcqa49mib13.cloudfront.net/spark-${APACHE_SPARK_VERSION}-bin-hadoop2.7.tgz | tar -xz -C /usr/local/
cd /usr/local
ln -s spark-${APACHE_SPARK_VERSION}-bin-hadoop2.7 spark


apt-get clean
# Spark env
export SPARK_HOME=/usr/local/spark
# TO BE CHECK ONCE INSTALLED
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.4-src.zip

# Install Python packages
conda install --yes 'ipython'
conda clean -yt

# fix permisions
chown -R vagrant:vagrant /opt/*