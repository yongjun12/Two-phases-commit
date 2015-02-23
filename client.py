import subprocess
import sys
import xmlrpclib
import sqlite3
import time
from ClientSetUp import *

# log transaction 
# parameter: 
#	operate_id: 1,2,3,4 
#	server: server address
def log(operate_id, server):
	c.execute("insert into log values('%d', '%s')" % (operate_id, server))
	conn.commit()

# Extract key value from server
# Delete existing record in local db if no key value is obtained
# Log table twice:
#    first logging(operate_id = 1) indicates fetch process started
#    second logging(operate_id = 2) indicates fetch process completed successfully.
# Trigger the server to log at last
def get():
	log(1, proxy_add)
	try:
		value = proxy.get(client_add)
		
		if(value is False): 
			print "No key on server, it might be deleted or never created!"
		else:
			print "get value: %s " % value

	except xmlrpclib.ProtocolError as err:
		print "Error occur:"
		print "Error code: %d" % err.errcode
		print "Error message: %s" % err.message
		return False

	# Delete key on local as key was deleted on server
	if( value is False ):
		c.execute("delete from info where key='key'")
		conn.commit()
		print "Key on local machine delete successfully"
	else:
		c.execute("insert or replace into info values('key', '%s')" % value)
		conn.commit()
		print "update value %s" % value

	log(2, proxy_add)

	# calls back server confirming process went well
	# The commit phase
	try:
		proxy.log(2, client_add)
	except xmlrpclib.ProtocolError as err:
		print "Error occur:"
		print "Error code: %d" % err.errcode
		print "Error message: %s" % err.message
		return False

	return True


# Insert or update key to server
# parameter: 
#	new_val: the value to insert 
# Log table twice:
#    first logging(operate_id=3) indicates put process started
#    second logging(operate_id=4) indicates put process completed successfully.
# Trigger the server to log at last

def put(new_val):

	log(3, proxy_add)

	try:
		proxy.put(new_val, client_add)
		print "put value: %s " % new_val
	except xmlrpclib.ProtocolError as err:
		print "Error occur:"
		print "Error code: %d" % err.errcode
		print "Error message: %s" % err.message
		return False

	# There is only one record holding the key.
	# Replace the tuple if key already exists.
	c.execute("insert or replace into info values('key','%s')" % new_val)
	conn.commit()

	log(4, proxy_add)
	print "put value success"

	try:
		proxy.log(4, client_add, 2)
	except xmlrpclib.ProtocolError as err:
		print "Error occur:"
		print "Error code: %d" % err.errcode
		print "Error message: %s" % err.message
		return False

	return True

# Delete key on server and local machine
# parameter: None. Delete if exist
# Log table twice:
#    first logging(operate_id=3) indicates delete process started
#    second logging(operate_id=4) indicates delete process completed successfully.
# Trigger the server to log at last
def delete():
	log(3, proxy_add)

	try:
		delVal = proxy.delete(client_add)
		print "delete value: %s" % delVal
	except xmlrpclib.ProtocolError as err:
		print "Error occur:"
		print "Error code: %d" % err.errcode
		print "Error message: %s" % err.message
		return False
	
	c.execute("delete from info where key = 'key'")
	conn.commit()

	log(4, proxy_add)
	print "delete value succes on client machine"

	try:
		proxy.log(4, client_add, 2)
	except xmlrpclib.ProtocolError as err:
		print "Error occur:"
		print "Error code: %d" % err.errcode
		print "Error message: %s" % err.message
		return False

	return True


