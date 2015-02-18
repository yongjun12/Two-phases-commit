import xmlrpclib
import sqlite3

from SimpleXMLRPCServer import SimpleXMLRPCServer

def log(operate_id, client):
	pass
	# conn = sqlite3.connect('server')
	# c = conn.cursor()
	# print operate_id + " " + client 
	# c.execute("insert into log values('%d', '%s')" % (operate_id, client))
	# c.commit()

def get(client):
	conn = sqlite3.connect('server')
	c = conn.cursor()	
#	log(1, client)
	return c.execute('select value from info').fetchone()[0]

def put(new_val):
	conn = sqlite3.connect('server')
	c = conn.cursor()

	while(1):
		last_row_id = c.execute('select max(rowid) from log').fetchone()[0]
		status = c.execute("select operate_id from log where rowid = %d" % last_row_id).fetchone()[0]
		if( status%2 == 0 ):
			break
		time.sleep(3)
		print "server is waiting function to complete"
		print "sleep 3 sec and try again"

	print "your turn to start put funciton"
	c.execute('')

server = SimpleXMLRPCServer(("134.87.178.254", 8000))
print "Listening on port 8000..."
server.register_function(log, "log")
server.register_function(get, "get")
server.serve_forever()

conn = sqlite3.connect('server')
c = conn.cursor()



# insert(cursor, "2")
# conn.commit()
# get(cursor)

