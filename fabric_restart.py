from fabric.api import run, env, sudo
from fabric.operations import put

env.hosts = ['10.211.55.100', '10.211.55.101', '10.211.55.102', '10.211.55.103']

env.user = 'vagrant'
env.password = 'vagrant'


def run_spark_master():
    sudo('cd /usr/local/spark/sbin && ./ start-master.sh')


def stop_spark_master():
    sudo('cd /usr/local/spark/sbin && ./ stop-master.sh')


def start_spark_slave():
    sudo('cd /usr/local/spark/sbin/ && ./start-slave.sh spark://10.211.55.100:7077')


def stop_spark_slave():
    sudo('cd /usr/local/spark/sbin && ./ stop-slave.sh')
