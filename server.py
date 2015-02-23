import sys
import xmlrpclib
import sqlite3
import subprocess
import time
from SimpleXMLRPCServer import SimpleXMLRPCServer

# Log Transaction
# parameter: 
#   operate_id: 1,2,3,4. 1&2 on log table; 3&4 on logEx table
#   client: client IP
#   logTable: 1 as log table, 2 as logEx table. 1 by default
# return value:
#    True for success and False will pop out errors

def log(operate_id, client, logTable = 1):
	
	conn = sqlite3.connect('server')
	c = conn.cursor()
	print "client: %s" % client 

	if(logTable == 1):
		log = "log"
	else:
		log = "logEx"  # Exclusive lock on logEx table. 

	c.execute("insert into %s values('%d', '%s')" % (log, operate_id, client))
	conn.commit()

	return True

# Fetch key 
# parameter: 
#	client: IP address of the machine that intializes fetch request
# return value:
#   key value if exists
#   False if no such key 
def get(client):

	conn = sqlite3.connect('server')
	c = conn.cursor()

	# set the record indicating fetch process started on server
	log(1, client)

	result = c.execute('select value from info').fetchone()
	if( result is None):
		return False
	else:
		return result[0]

# Update key on server
# parameter:
#   new_val: the value to insert
#   client: IP address of the machine that initializes the request
# return value:
#    True for success and False will pop out errors    
def put(new_val, client):

	conn = sqlite3.connect('server')
	c = conn.cursor()

	while(1):

		last_row_id = c.execute('Select rowid from logEx order by rowid desc limit 1').fetchone()
		if( last_row_id is None ):
			status = 4
		else:
			status = c.execute("select operate_id from logEx where rowid = %d" % last_row_id[0]).fetchone()[0]

		# breaks when previous transaction is completed
		if( status == 4 ):
			break

		time.sleep(3)
		print "server is waiting function to complete"
		print "sleep 3 sec and try again"

	print "your turn to start put funciton"
	c.execute("insert or replace into info values('key','%s')" % new_val)
	conn.commit()

	log(3, client, 2)

	return True

# Delete key on server
# parameter:
#	client: IP address of the machine that initializes request
# return value:
#    True for success and False will pop out errors
def delete(client):
	conn = sqlite3.connect('server')
	c = conn.cursor()

	while(1):

		last_row_id = c.execute('select max(rowid) from logEx').fetchone()[0]
		if(last_row_id is None):
			status = 4
		else:
			status = c.execute("select operate_id from logEx where rowid = %d" % last_row_id).fetchone()[0]

		if( status == 4 ):
			break

		time.sleep(3)
		print "server is waiting function to complete"
		print "sleep 3 sec and try again"

	print "your turn to start put funciton"
	c.execute("delete from info where key = 'key'")
	conn.commit()

	log(3, client, 2)
	return True

# Extract server ip using shell command
cmd = "/sbin/ifconfig en0 | grep 'inet '| cut -d ' ' -f 2"
server_add = subprocess.check_output(cmd, shell="True")
# get rid of newline 
server_add = server_add.rstrip('\n')

# Setup remote procedure call server to listen events
server = SimpleXMLRPCServer((server_add, 8000))
print "Listening on port 8000..."

# Register function to enable communication from client
server.register_function(log, "log")
server.register_function(get, "get")
server.register_function(put, "put")
server.register_function(delete, "delete")

# Start server
server.serve_forever()


