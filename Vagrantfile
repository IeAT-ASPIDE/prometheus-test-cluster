# ASPIDE Prometheus testbed cluster
# beta v0.0.1
# Bootstrap script for Prometheus cluster
#
#Copyright 2019, Institute e-Austria, Timisoara, Romania
#    http://www.ieat.ro/
#Developers:
# * Gabriel Iuhasz, iuhasz.gabriel@info.uvt.ro
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at:
#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

$master_script = <<SCRIPT
#!/bin/bash
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
# add-apt-repository ppa:jonathonf/python-3.6 -y
apt-get update
apt-get install screen -y
# apt-get install wget -y
apt-get install python3-pip -y

sudo chown vagrant:vagrant -R /opt
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
      - targets: ['10.211.55.101:9100', '10.211.55.102:9100', '10.211.55.103:9100']
EOF
cd /opt/prometheus-2.13.0-rc.0.linux-amd64
# Start prometheus
# nohup ./prometheus > prometheus.log 2>&1 &

# Register node_exporter as service
sudo mkdir /usr/lib/systemd/system
sudo cp /vagrant/prometheus.service /usr/lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable prometheus.service
sudo service prometheus.service start

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
SCRIPT


$hosts_script = <<SCRIPT
#!/bin/bash
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
apt-get update
apt-get install wget -y
apt-get install collectd -y
apt-get install python3-pip -y

sudo chown vagrant:vagrant -R /opt
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
sudo cp /vagrant/node_exporter.service /usr/lib/systemd/system/
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
nohup dask-worker 10.211.55.100:8786 > dask-worker.log 2>&1 &

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
SCRIPT
#TODO add exports to bashrc:
#
#export PYSPARK_DRIVER_PYTHON=/usr/bin/ipython
#export PYSPARK_PYTHON=/opt/conda/bin/python
$spark_master_script = <<SCRIPT
#!/bin/bash


# Start Spark Master
cd /usr/local/spark/sbin/ &&  ./start-master.sh

SCRIPT

$spark_slave_script = <<SCRIPT
#!/bin/bash



# Start Spark Master
cd /usr/local/spark/sbin/ && ./start-slave.sh spark://10.211.55.100:7077

SCRIPT

Vagrant.configure("2") do |config|

  # Define base image
  config.vm.box = "ubuntu/bionic64"
  #config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  # Manage /etc/hosts on host and VMs
  config.hostmanager.enabled = false
  config.hostmanager.manage_host = true
  config.hostmanager.include_offline = true
  config.hostmanager.ignore_private_ip = false

  #Set same Username and Password
  #config.ssh.username = "dice"
  #config.ssh.password = "diceh2020"
  
  #Path to Private SSH key location
  #config.ssh.private_key_path = "<path/to/key>"
  
  #SSH default host and port settings
  #config.ssh.host ="<host>"
  #config.ssh.port = "<port>"
  
  
  config.vm.define :master do |master|
    master.vm.provider :virtualbox do |v|
      v.name = "prometheus"
      v.customize ["modifyvm", :id, "--memory", "4096"]
    end
    master.disksize.size = '20GB'
    master.vm.network :private_network, ip: "10.211.55.100"
    master.vm.hostname = "prometheus"
    master.vm.network :forwarded_port, host:9090, guest: 9090
    master.vm.network :forwarded_port, host:3000, guest: 3000
    master.vm.network :forwarded_port, host:8787, guest:8787
    master.vm.network :forwarded_port, host:8786, guest:8786
    master.vm.network :forwarded_port, guest: 22, host: 2185
    master.vm.network :forwarded_port, guest: 8888, host: 8897
    master.vm.network :forwarded_port, guest: 8080, host: 8081
    master.vm.network :forwarded_port, guest: 7070, host: 7070
    master.vm.network :forwarded_port, guest: 4040, host: 4040
    master.vm.network :forwarded_port, guest: 18080, host: 18080
    master.vm.provision :shell, :inline => $master_script
    master.vm.provision :shell, path: "provision_script.sh"
    master.vm.provision :shell, :inline => $spark_master_script
    master.vm.provision :hostmanager
  end

  config.vm.define :slave1 do |slave1|
    slave1.vm.box = "ubuntu/bionic64"
    slave1.vm.provider :virtualbox do |v|
      v.name = "node1"
      v.customize ["modifyvm", :id, "--memory", "4096"]
    end
    slave1.vm.network :private_network, ip: "10.211.55.101"
    slave1.vm.hostname = "node1"
    slave1.vm.network :forwarded_port, guest: 22, host: 2186
    slave1.vm.network :forwarded_port, guest: 8080, host: 8082
    slave1.vm.network :forwarded_port, guest: 7070, host: 7071
    slave1.vm.network :forwarded_port, guest: 4040, host: 4041
    slave1.vm.network :forwarded_port, guest: 18080, host: 18081
    slave1.vm.provision :shell, :inline => $hosts_script
    slave1.vm.provision :shell, path: "provision_script.sh"
    slave1.vm.provision :shell, :inline => $spark_slave_script
    slave1.vm.provision :hostmanager
  end

  config.vm.define :slave2 do |slave2|
    slave2.vm.box = "ubuntu/bionic64"
    slave2.vm.provider :virtualbox do |v|
      v.name = "node2"
      v.customize ["modifyvm", :id, "--memory", "4096"]
    end
    slave2.vm.network :private_network, ip: "10.211.55.102"
    slave2.vm.hostname = "node2"
    slave2.vm.network :forwarded_port, guest: 22, host: 2187
    slave2.vm.network :forwarded_port, guest: 8080, host: 8083
    slave2.vm.network :forwarded_port, guest: 7070, host: 7072
    slave2.vm.network :forwarded_port, guest: 4040, host: 4042
    slave2.vm.network :forwarded_port, guest: 18080, host: 18082
    slave2.vm.provision :shell, :inline => $hosts_script
    slave2.vm.provision :shell, path: "provision_script.sh"
    slave2.vm.provision :shell, :inline => $spark_slave_script
    slave2.vm.provision :hostmanager
  end

  config.vm.define :slave3 do |slave3|
    slave3.vm.box = "ubuntu/bionic64"
    slave3.vm.provider :virtualbox do |v|
      v.name = "node3"
      v.customize ["modifyvm", :id, "--memory", "4096"]
    end
    slave3.vm.network :private_network, ip: "10.211.55.103"
    slave3.vm.hostname = "node3"
    slave3.vm.network :forwarded_port, guest: 22, host: 2188
    slave3.vm.network :forwarded_port, guest: 8080, host: 8084
    slave3.vm.network :forwarded_port, guest: 7070, host: 7073
    slave3.vm.network :forwarded_port, guest: 4040, host: 4043
    slave3.vm.network :forwarded_port, guest: 18080, host: 18083
    slave3.vm.provision :shell, :inline => $hosts_script
    slave3.vm.provision :shell, path: "provision_script.sh"
    slave3.vm.provision :shell, :inline => $spark_slave_script
    slave3.vm.provision :hostmanager
  end

end
