import sys
import xmlrpclib
import sqlite3
import subprocess
import time

from SimpleXMLRPCServer import SimpleXMLRPCServer

def log(operate_id, client, logTable = 1):
	print "log"
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

def get(client):
	conn = sqlite3.connect('server')
	c = conn.cursor()
	log(1, client)
	result = c.execute('select value from info').fetchone()
	if( result is None):
		return False
	else:
		return result[0]

def put(new_val, client):
	conn = sqlite3.connect('server')
	c = conn.cursor()

	while(1):
		last_row_id = c.execute('select max(rowid) from logEx').fetchone()
		if( last_row_id is None ):
			status = 4
		else:
			status = c.execute("select operate_id from logEx where rowid = %d" % last_row_id[0]).fetchone()[0]
		print status
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

def delete(client):
	conn = sqlite3.connect('server')
	c = conn.cursor()

	while(1):
		last_row_id = c.execute('select max(rowid) from logEx').fetchone()[0]
		if(last_row_id is None):
			status = 4
		else:
			status = c.execute("select operate_id from logEx where rowid = %d" % last_row_id).fetchone()[0]
		print status
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

cmd = "/sbin/ifconfig en0 | grep 'inet '| cut -d ' ' -f 2"
server_add = subprocess.check_output(cmd, shell="True")
# get rid of newline 
server_add = server_add.rstrip('\n')

server = SimpleXMLRPCServer((server_add, 8000))
print "Listening on port 8000..."
server.register_function(log, "log")
server.register_function(get, "get")
server.register_function(put, "put")
server.register_function(delete, "delete")
server.serve_forever()




# insert(cursor, "2")
# conn.commit()
# get(cursor)

