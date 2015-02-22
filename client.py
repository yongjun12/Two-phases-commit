import subprocess
import sys
import xmlrpclib
import sqlite3
import time
from ClientSetUp import *


def log(operate_id, server):
	c.execute("insert into log values('%d', '%s')" % (operate_id, server))
	conn.commit()

def get():
	log(1, proxy_add)
	try:
		print "df"
		value = proxy.get(client_add)
		print value
		if(value is False): 
			print "Key is deleted!"
		else:
			print "get value: %s " % value
	except xmlrpclib.ProtocolError as err:
		print "Error occur:"
		print "Error code: %d" % err.errcode
		print "Error message: %s" % err.message
		return False
	if( value is False ):
		c.execute("delete from info where key='key'")
		print "delete key"
	else:
		c.execute("insert or replace into info values('key', '%s')" % value)
		print "update value %s" % value

	log(2, proxy_add)
	print "get value success"
	try:
		proxy.log(2, client_add)
	except xmlrpclib.ProtocolError as err:
		print "Error occur:"
		print "Error code: %d" % err.errcode
		print "Error message: %s" % err.message
		return False

	return True


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



