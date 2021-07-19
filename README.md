# prometheus-test-cluster
This is a vagrant based portable testbed cluster for prometheus

# Prerequisets
* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)
* [Vagrant Host Manager](https://github.com/devopsgroup-io/vagrant-hostmanager)

# Usage
* Clone the repository
* In the repo directory run:
  * vagrant up
* To access Prometheus API go to
  * localost:9090
* To access Graphite got to
  * localhost:3000
# Spark Usage
* Go to SPARK_HOME
  * /usr/local/spark/sbin
* To start master
  * sudo ./start-master.sh -h <MASTER_IP>
* All other VMs
  * sudo ./start-slave.sh spark://<MASTER_IP>:7077
* To check log go to /usr/local/spark-3.1.1-bin-hadoop2.7/logs/
* To run Spark Job
    * spark-submit --class org.apache.spark.examples.SparkPi --master spark://<MASTER_IP>:7077 /usr/local/spark/examples/jars/spark-examples_2.12-3.1.1.jar 100
    * If during execution you get an error related to incompatibilities related to minor Pythin version
    make suer you have the correct PYSPARK_PYTHON env. var.  set.
        * export PYSPARK_PYTHON=/opt/conda/bin/python
* Submitting Python based applications
    * ./spark-submit --master spark://<master>:7077 ../examples/src/main/python/pi.py 1000


# Note

On some systems and certain situations Spark has issues with handling hostnames. users have to keep this in mind when 
executing distributed applications. The executors will be created but will exit immediately. Thus all jobs will be run on the
local (master) machine. Simplest solution is to edit the /etc/hosts file:

# Spark Cluster
<IP_MASTER>  spark-master
<IP_SLAVE_1> spark-slave-1
<IP_SLAVE_2> spark-slave-2
<IP_SLAVE_3> spark-slave-3
