from fabric.api import env, roles, run, put, cd, parallel
import subprocess
from sys import platform

# This project set server nodes as the machine that runs fabfile by default
# Extract local IP 

cmd = "/sbin/ifconfig en0 | grep 'inet '| cut -d ' ' -f 2"
server_add = subprocess.check_output(cmd, shell="True")
server_add = server_add.rstrip('\n')

env.hosts = [
	server_add,
]

env.roledefs.update({
	'server': [server_add],
	'client': ["192.168.22.138", server_add],
})

# Set authentication key and config file as you wish
# env.use_ssh_config = True
# env.ssh_config_path = <config_file>
# env.key_filename = <key_file>


def hello():
	run("echo 'Hello world'")

# default dir: home directory
# put function only executes if files don't exist 
# To update, delete existing files before calling put funtion
# Delete files by uncommenting the first line
 
@roles('client')
def setup():
	if platform == "linux" or platform == "linux2":
		# run('rm client.py && rm ClientSetUp.py && rm ./DbSetUp.sh')
		put('./client.py')
		put('./ClientSetUp.py')
		put('./DbSetUp.sh')
		run('chmod u+x ./DbSetUp.sh; ./DbSetUp.sh')
	elif platform =="darwin":
		# run('rm client.py && rm ClientSetUp.py && rm ./DbSetUp.sh')
		put('./client.py')
		put('./ClientSetUp.py')
		put('./DbSetUp.sh')
		run('chmod u+x ./DbSetUp.sh;')
		run('./DbSetUp.sh')

@roles('client')
def getKey():
	run("python -c \"import client; client.get()\"")

## How to pass in key value?
@roles('client')
def putKey():
	run("python -c \"import client; client.put(5)\"")

@roles('client')
def delKey():
	run("python -c \"import client; client.delete()\"")