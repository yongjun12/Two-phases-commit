import xmlrpclib
import sqlite3
import time


def log(operate_id, server):
	c.execute("insert into log values('%d', '%s')" % (operate_id, server))
	conn.commit()

def get():
	log(1, proxy_add)

	while(1) {
	
	try:
		value = proxy.get(client_add)
		print "get value: %s " % value
	except xmlrpclib.ProtocolError as err:
		print "Error occur:"
		print "Error code: %d" % err.errcode
		print "Error message: %s" % err.message
		if(++error_retry < 5):
			time.sleep(5)
		else:
			return false
	}

	c.execute("update info set value = '%s' " % value)
	log(2, proxy_add)
	print "get value success"
	proxy.log(2, client_add)


def put(new_val):
	log(3, proxy_add)




proxy = xmlrpclib.ServerProxy("http://134.87.178.254:8000/", allow_none = True)
proxy_add = "134.87.178.254:8000"
client_add = "client A"
# print "3 is even: %s" % str(proxy.is_even(3))
# print "100 is even: %s" % str(proxy.is_even(100))

conn = sqlite3.connect('ex')

c = conn.cursor() 
get()