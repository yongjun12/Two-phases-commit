from fabric.api import env, roles, run, put, cd, parallel
import subprocess
from sys import platform

cmd = "/sbin/ifconfig en0 | grep 'inet '| cut -d ' ' -f 2"
server_add = subprocess.check_output(cmd, shell="True")
s = server_add.rstrip('\n')

env.hosts = [
	s,
	# "slice320.pcvm3-1.instageni.metrodatacenter.com",
 #    "slice320.pcvm2-2.instageni.rnoc.gatech.edu",
]

env.roledefs.update({
	'server': [s],
	# 'client': [ "slice320.pcvm3-1.instageni.metrodatacenter.com",
	# 			"slice320.pcvm2-2.instageni.rnoc.gatech.edu"],
	'client': ["192.168.22.138", s],
	'localClient': [s]
})

# env.use_ssh_config = True
# env.ssh_config_path = "./ssh-config"
# env.key_filename="./id_rsa"


def hello():
	run("echo 'ddd'")

# default user: yongjun
@roles('client')
def setup():
	if platform == "linux" or platform == "linux2":
		run('rm client.py && rm ClientSetUp.py && rm ./DbSetUp.sh')
		put('./client.py')
		put('./ClientSetUp.py')
		put('./DbSetUp.sh')
		run('chmod u+x ./DbSetUp.sh; ./DbSetUp.sh')
	elif platform =="darwin":
		run('rm client.py && rm ClientSetUp.py && rm ./DbSetUp.sh')
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