#!/bin/bash
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
# add-apt-repository ppa:jonathonf/python-3.6 -y
apt-get update
apt-get install byobu -y
# apt-get install wget -y
apt-get install python3-pip -y

sudo chown ubuntu:ubuntu -R /opt
cd /opt
wget https://github.com/prometheus/prometheus/releases/download/v2.13.0-rc.0/prometheus-2.13.0-rc.0.linux-amd64.tar.gz
tar -xzvf prometheus-2.13.0-rc.0.linux-amd64.tar.gz && cd /opt/prometheus-2.13.0-rc.0.linux-amd64

cat <<EOF > /opt/prometheus-2.13.0-rc.0.linux-amd64/prometheus.yml
global:
  scrape_interval:     1s # By default, scrape targets every 15 seconds.
  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'aspide-monitor'
# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'node-prometheus'
    static_configs:
      - targets: [10.251.0.184:9100', '10.251.0.142:9100', '10.251.0.78:9100', '10.251.0.176:9100', '10.251.0.63:9100']
EOF
cd /opt/prometheus-2.13.0-rc.0.linux-amd64
# Start prometheus
nohup ./prometheus > prometheus.log 2>&1 &

cd /opt

# Download grafana
wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_4.2.0_amd64.deb -O /opt/grafana_4.2.0_amd64.deb

sudo apt-get install -y adduser libfontconfig

# Install grafana 
sudo dpkg -i grafana_4.2.0_amd64.deb

# Start grafana service 
sudo service grafana-server start

# Run on every boot
sudo update-rc.d grafana-server defaults

# Install dependancies
pip3 install numpy==1.16
pip3 install scikit-learn==0.21.3
pip3 install tpot
pip3 install dask[complete]
pip3 install dask distributed --upgrade
pip3 install dask-ml[complete] 
pip3 install dask-xgboost
pip3 install bokeh



# Start dask-schedueler
nohup dask-scheduler --host 0.0.0.0 --port 8786 > dask_schedueler.log 2>&1 &

# Set Swappiness value to 10 instead of 60
sysctl -w vm.swappiness=10
cat /proc/sys/vm/swappiness

cat > /etc/hosts <<EOF
127.0.0.1       localhost
# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
EOF