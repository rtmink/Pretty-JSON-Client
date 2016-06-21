#!/usr/bin/python  

"""
This file runs an a test case for the HTTP client. 
It connects to the server multiple times to get the 
expected JSON objects to be compared with the output
of the client. Keys in both the expected and client 
objects are ordered so they can be compared. If both
objects are equal then client has passed the test. By 
default 100 objects are obtained from the server and 
compared with the client objects to ensure all possible
types of objects are parsed correctly.

This code will run in Python 3, and possibly also in 2.7.
"""         

from __future__ import unicode_literals
from __future__ import print_function

import unittest
import os
import sys
import time
import json
import argparse
import subprocess

LIMIT = 100

# Handle version differences between Python 2 and 3
if sys.version_info.major >= 3:
    from http.client import HTTPConnection
else:
    from httplib import HTTPConnection

def runServer(limit, seed):
	os.system("python3 ugly_json_server.py --limit {0} --seed {1} &> /dev/null &".format(limit, seed))

def terminateServer():
	os.system("pkill -f ugly_json_server.py")

def runClient():
	proc = subprocess.Popen(["python3 pretty_json_client.py", ""], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
	out, err = proc.communicate()
	
	return out

def getExpectedObjects():
	"""
	Expected JSON objects are obtained by running the server
	repeatedly with seed 1 and increasing limit up to the
	specified LIMIT. In each call, we connect to the server
	to obtain the output. Initially the output is a single 
	object which we store in a list. The length of this
	output is the index of the second object outputted in 
	the next call to the server, and so on. Eventually we
	will have a list of expected objects.

	We then run the server with seed = 1 and limit = LIMIT,
	and run the client to obtain the pretty JSON objects.

	Since the pretty JSON objects are separated by line breaks
	and that the line breaks do not appear anywhere else, we
	can split the output to a list.

	Lastly, we order the keys in each of the JSON object and 
	compare the pretty objects with the expected objects.

	If they are all equal, we pass the test.
	"""

	expectedObjects = []
	objectTotalLen = 0

	for num in range(1,LIMIT+1):
		print("Obtaining expected JSON object {0}".format(num))

		# Run the server
		runServer(num, 1)

		# Ensure the server runs properly before running the client
		time.sleep(0.5)

		# Connect to the server to obtain the expected JSON object(s)
		conn = HTTPConnection("127.0.0.1: 8001")
		conn.request('GET', "/")
		response = conn.getresponse()

		resb = b""

		while True:
			temp = response.read(1024)

			if (len(temp)):
				resb += temp
			else:
				break

		# Close client's connection with the server
		conn.close()

		# Terminate the server
		terminateServer()

		# Decode output
		ress = resb.decode('utf-8')

		# Sort keys in the expected object
		newObject = json.dumps(json.loads(ress[objectTotalLen:]), sort_keys=True)

		# Store the object in the list
		expectedObjects.append(newObject)

		objectTotalLen = len(ress)

	return expectedObjects

class TestClient(unittest.TestCase):

	def test_client(self):
		expectedObjects = getExpectedObjects()

		# Run the server
		runServer(LIMIT, 1)

		# Ensure the server runs properly before running the client
		time.sleep(1)

		# Run the client
		out = runClient()

		# Terminate the server
		terminateServer()

		# Split the output into list of objects
		outputObjects = out.rstrip("\n").split("\n")
		
		for obj, expectedObj in zip(outputObjects, expectedObjects):
			# Order the keys in the output objects before
			# comparing them with the expected objects
			cleanObj = json.dumps(json.loads(obj), sort_keys=True)

			self.assertEqual(cleanObj, expectedObj)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--limit", help="number of JSON objects to test", type=int, default=100)
	args = parser.parse_args()
	LIMIT = args.limit
	del sys.argv[1:]
	unittest.main()

	


