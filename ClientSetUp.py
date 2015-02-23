# This file is to extract IP address based on platforms 
# and build two-way communication to server
# All variable defined here is to be imported by client.py

import xmlrpclib
import sqlite3
import subprocess
from sys import platform, argv

conn = sqlite3.connect('ex')
c = conn.cursor()

if platform == "linux" or platform == "linux2":
	print "using linux"
	cmd = "/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
elif platform =="darwin":
	print "using osx"
	cmd = "/sbin/ifconfig en0 | grep 'inet '| cut -d ' ' -f 2"

client_add = subprocess.check_output(cmd, shell="True")
client_add = client_add.rstrip('\n')

# Please input server ip by hand
proxy_ip = "192.168.0.113"
proxy_add = "http://" + proxy_ip + ":8000/" 

proxy = xmlrpclib.ServerProxy(proxy_add, allow_none = True)
print "Connecting to server %s on 8000" % proxy_ip

