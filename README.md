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
* To check log go to /usr/local/spark-2.1.1-bin-hadoop2.7/logs/
* To run Spark Job
    * spark-submit --class org.apache.spark.examples.SparkPi --master spark://<MASTER_IP>:7077 /usr/local/spark/examples/jars/spark-examples_2.11-2.1.1.jar 100
    * If during execution you get an error related to incompatibilities related to minor Pythin version
    make suer you have the correct PYSPARK_PYTHON env. var.  set.
        * export PYSPARK_PYTHON=/opt/conda/bin/python
* Submitting Python based applications
    * ./bin/spark-submit --master spark://<MASTER_IP>:7077 loc/of/file/pySparkPi.py 1000

