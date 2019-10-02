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
apt-get update
apt-get install screen -y
# apt-get install wget -y

cd /opt
wget https://github.com/prometheus/prometheus/releases/download/v2.13.0-rc.0/prometheus-2.13.0-rc.0.linux-amd64.tar.gz
tar -xzvf prometheus-2.13.0-rc.0.linux-amd64
cd prometheus-2.13.0-rc.0.linux-amd64

cat <<EOF > prometheus.yml
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.
  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'codelab-monitor'
# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'node-prometheus'
    static_configs:
      - targets: ['10.211.55.101:9100', '10.211.55.102:9100', '10.211.55.103:9100']
EOF

# tart prometheus
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
apt-get update
apt-get install wget -y
apt-get install collectd


cd /opt
wget https://github.com/prometheus/node_exporter/releases/download/v0.18.1/node_exporter-0.18.1.linux-amd64.tar.gz

# Extract node_exporter
tar -xvzf node_exporter-0.18.1.linux-amd64.tar.gz

# create a symbolic link of node_exporter
sudo ln -s /opt/node_exporter/node_exporter-0.18.1.linux-amd64/node_exporter /usr/bin

# Edit node_exporter configuration file and add configuration so that it will automatically start in next boot
cat <<EOF > /etc/init/node_exporter.conf
# Run node_exporter-0.14.0.linux-amd64
start on startup
script
   /usr/bin/node_exporter
end script
EOF

# Start service of node_exporter
sudo service node_exporter start

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

Vagrant.configure("2") do |config|

  # Define base image
  config.vm.box = "ubuntu/xenial64"
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
    master.vm.network :private_network, ip: "10.211.55.100"
    master.vm.hostname = "prometheus"
    master.vm.network :forwarded_port, host:9090, guest: 9090
    master.vm.network :forwarded_port, host:3000, guest: 3000
    master.vm.network :forwarded_port, guest: 22, host: 2185
    master.vm.provision :hostmanager
    master.vm.provision :shell, :inline => $master_script
  end

  config.vm.define :slave1 do |slave1|
    slave1.vm.box = "ubuntu/xenial64"
    slave1.vm.provider :virtualbox do |v|
      v.name = "node1"
      v.customize ["modifyvm", :id, "--memory", "2048"]
    end
    slave1.vm.network :private_network, ip: "10.211.55.101"
    slave1.vm.hostname = "node1"
    slave1.vm.network :forwarded_port, guest: 22, host: 2186
    slave1.vm.provision :shell, :inline => $hosts_script
    slave1.vm.provision :hostmanager
  end

  config.vm.define :slave2 do |slave2|
    slave2.vm.box = "ubuntu/xenial64"
    slave2.vm.provider :virtualbox do |v|
      v.name = "node2"
      v.customize ["modifyvm", :id, "--memory", "2048"]
    end
    slave2.vm.network :private_network, ip: "10.211.55.102"
    slave2.vm.hostname = "node2"
    slave2.vm.network :forwarded_port, guest: 22, host: 2187
    slave2.vm.provision :shell, :inline => $hosts_script
    slave2.vm.provision :hostmanager
  end

  config.vm.define :slave3 do |slave3|
    slave3.vm.box = "ubuntu/xenial64"
    slave3.vm.provider :virtualbox do |v|
      v.name = "node3"
      v.customize ["modifyvm", :id, "--memory", "2048"]
    end
    slave3.vm.network :private_network, ip: "10.211.55.103"
    slave3.vm.hostname = "node3"
    slave3.vm.network :forwarded_port, guest: 22, host: 2188
    slave3.vm.provision :shell, :inline => $hosts_script
    slave3.vm.provision :hostmanager
  end

end
