#!/bin/bash
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
apt-get update
apt-get install wget -y
apt-get install collectd -y
apt-get install python3-pip -y

sudo chown ubuntu:ubuntu -R /opt
cd /opt
wget https://github.com/prometheus/node_exporter/releases/download/v0.18.1/node_exporter-0.18.1.linux-amd64.tar.gz

# Extract node_exporter
tar -xvzf node_exporter-0.18.1.linux-amd64.tar.gz

# create a symbolic link of node_exporter
# sudo ln -s /opt/node_exporter/node_exporter-0.18.1.linux-amd64/node_exporter /usr/bin

# Edit node_exporter configuration file and add configuration so that it will automatically start in next boot
# cat <<EOF > /etc/init/node_exporter.conf
# start on startup
# script
#    /usr/bin/node_exporter
# end script
# EOF
# Start service of node_exporter
# sudo service node_exporter start

#cd /opt/node_exporter-0.18.1.linux-amd64/

#nohup ./node_exporter > exporter.log 2>&1 &

# Register node_exporter as service 
sudo mkdir /usr/lib/systemd/system
sudo cp /home/ubuntu/n_scripts/openstack_services/node_exporter.service /usr/lib/systemd/system/
#sudo cp /vagrant/node_exporter.service /usr/lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable node_exporter.service
sudo service node_exporter start  


# Install dependancies
pip3 install numpy==1.16
pip3 install scikit-learn==0.21.3
pip3 install tpot
pip3 install dask[complete]
pip3 install dask distributed --upgrade
pip3 install dask-ml[complete]
pip3 install dask-xgboost 
pip3 install bokeh



# Start dask-worker
nohup dask-worker 10.251.0.107:8786 > dask-worker.log 2>&1 &

#Set Swappiness value to 10 instead of 60
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