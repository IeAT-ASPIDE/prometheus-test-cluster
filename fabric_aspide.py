from fabric.api import run, env, sudo
from fabric.operations import put


# Hosts
env.hosts = ['IP_1', 'IP_2']


# Credentials
env.user = 'USER'
env.key_filename = 'KEY.pem'

# Variables
script_directory_path = '/home/ubuntu/n_scripts'
openstack_script_path = '~/openstack_scripts'
openstack_services_path = '~/openstack_services'
kernel_path = '~/kernels'
# Functions


def check_scripts():
    cmd = "ls -laht {}".format(script_directory_path)
    run(cmd)


def get_users():
    run('whoami')


def delete():
    run('rm -rf /home/ubuntu/n_scripts')


def copy():
    mkdir_cmd = 'mkdir -p {}'.format(script_directory_path)
    run(mkdir_cmd)
    put(openstack_script_path, script_directory_path)
    put(openstack_services_path, script_directory_path)
    put(kernel_path, script_directory_path)
    ls_cmd = "ls {}".format(script_directory_path)
    run(ls_cmd)


def run_provision():
    prov_cmd = "chmod +x {}/openstack_scripts/provision_script.sh".format(script_directory_path)
    sudo(prov_cmd)
    prov_exec_cmd = "cd {}/openstack_scripts/ && ./provision_script.sh".format(script_directory_path)
    sudo(prov_exec_cmd)


def run_slave():
    slave_cmd = "chmod +x {}/openstack_scripts/slave_script.sh".format(script_directory_path)
    sudo(slave_cmd)
    slave_exec_cmd = "cd {}/openstack_scripts/ && ./slave_script.sh".format(script_directory_path)
    sudo(slave_exec_cmd)


def run_spark_master():
    sudo('chmod +x /home/ubuntu/n_scripts/openstack_scripts/spark_master.sh')
    sudo('cd /home/ubuntu/n_scripts/openstack_scripts/ && ./spark_master.sh')


def run_spark_slave():
    sudo('chmod +x /home/ubuntu/n_scripts/openstack_scripts/spark_slave.sh')
    sudo('cd /home/ubuntu/n_scripts/openstack_scripts/ && ./spark_slave.sh')