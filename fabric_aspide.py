from fabric.api import run, env, sudo
from fabric.operations import put


# Hosts
# env.hosts = ['10.251.0.184', '10.251.0.142', '10.251.0.78', '10.251.0.176', '10.251.0.63']
# env.hosts = ['194.102.62.207']
# env.hosts = ['194.102.62.155', '194.102.62.162', '194.102.62.253', '194.102.62.183', '194.102.62.174', '194.102.62.207']
env.hosts = ['194.102.62.155', '194.102.62.162', '194.102.62.253', '194.102.62.183', '194.102.62.174']


# Credentials
env.user = 'ubuntu'
env.key_filename = '/Users/Gabriel/Dropbox/PGP_Key/openstack/igabriel1985a.pem'

# Variables
script_directory_path = '/home/ubuntu/n_scripts'
openstack_script_path = '/Users/Gabriel/Documents/workspaces/prometheus-test-cluster/openstack_scripts'
openstack_services_path = '/Users/Gabriel/Documents/workspaces/prometheus-test-cluster/openstack_services'
kernel_path = '/Users/Gabriel/Documents/workspaces/prometheus-test-cluster/kernels'
# Functions


def check_scripts():
    cmd = "ls -laht {}".format(script_directory_path)
    run(cmd)


def get_users():
    run('whoami')


def delete():
    run('rm -rf /home/ubuntu/n_scripts')
    run('rm -rf /home/ubuntu/scripts')


# def copy_fix():
#     # put('/Users/Gabriel/Documents/workspaces/prometheus-test-cluster/kernels', '/home/ubuntu/n_scripts')
#     run('cp /home/ubuntu/n_scripts/kernels/scala.json /opt/conda/share/jupyter/kernels/scala/scala.json')
#     run('cp /home/ubuntu/n_scripts/kernels/pyspark.json /opt/conda/share/jupyter/kernels/pyspark/pyspark.json')
#

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


def clone_chaos():
    run('cd /opt && git clone https://github.com/IeAT-ASPIDE/ede-chaos-inductor.git')


def pull_chaos():
    run('cd /opt/ede-chaos-inductor && git pull')


def install_redis():
    sudo('apt-get update')
    sudo('apt-get install redis-server -y')
    sudo('systemctl enable redis-server.service')


def create_conda_env():
    run('conda create -n chaos -y')
    # run('conda install -n chaos numpy flask rq redis pyyaml flask_restul')


def install():
    # run('source activate chaos && pip install flask rq redis pyyaml flask-restful scipy flask-restful-swagger psutil py-cpuinfo pygrok')
    run('source activate chaos && pip install pygrok')


def move_chaos_rq_worker():
    sudo('cp /opt/ede-chaos-inductor/etc/systemd/chaosrqworker@.service /usr/lib/systemd/system')
    sudo('systemctl enable chaosrqworker@.service')
    sudo('systemctl daemon-reload')


def move_eci():
    sudo('cp /opt/ede-chaos-inductor/etc/systemd/eci@.service /usr/lib/systemd/system')
    sudo('systemctl enable eci@.service')
    sudo('systemctl daemon-reload')


def copy_secret():
    put('/Users/Gabriel/Documents/workspaces/ede-chaos-inductor/etc/s.x', '/opt/ede-chaos-inductor/etc')


def start_eci():
    sudo('service eci@0 start')


def status_eci():
    sudo('service eci@0 status')


def stop_eci():
    sudo('service eci@0 stop')