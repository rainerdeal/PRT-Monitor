''' 
	PRT Monitor
	
	A bot written in Python that uses Twython and JSON to compile data on WVU's PRT Status.
	Copyright 2017, Ricky Deal, All rights reserved.
'''

import time, urllib, json, csv, os, unicodedata
from collections import deque
from twython import Twython
from auth import (
	consumer_key,
	consumer_secret,
	access_token_key,
	access_token_secret)

"""	Creates and updates the CSV file
	
	Converts the JSON data to CSV and saves it to 'monitor.csv'
"""
def toCSV(data):

	# if CSV file exists then just write to it
	if os.path.isfile('monitor.csv') == True:
		csvData = open('monitor.csv', 'a')
		csvWriter = csv.writer(csvData)		# Create the CSV writer object
		csvWriter.writerow(data.values())
	
	# else create the CSV file first, then write to it
	else:
		csvData = open('monitor.csv', 'a')
		csvWriter = csv.writer(csvData)		# Create the CSV writer object
		csvWriter.writerow(data.keys())
		csvWriter.writerow(data.values())
	csvData.close()

"""	Returns lastRow
	
	Return the last status recorded in 'monitor.csv'
"""
def _get_last_row(csv_filename):
	
	with open(csv_filename, 'r') as f:
		try:
			lastRow = deque(csv.reader(f), 1)[0]
		except IndexError:  # empty file
			lastRow = None
		return lastRow

"""	Tweet the PRT Status
	
	Formats the tweet in a user friendly way and tweets.
	(note: Only tweets first sentence of data[message].)
"""
def tweetStatus(data):
	
	Twitter = Twython(
		consumer_key,
		consumer_secret,
		access_token_key,
		access_token_secret)

	mess = data['message']																					# Message raw
	message_s = unicodedata.normalize('NFKD', mess).encode('ascii','ignore') 								# Message string
	message_f = "%s (%s). #wvuprt #wvu" %(message_s.split(".", 1)[0], time.ctime(int(data['timestamp'])))	# Message formatted

	Twitter.update_status(status=message_f)
	#print(message_f)
	
# ********************************* START *********************************

oldTimestamp = ""
timestamp = int(time.time())
url = "http://prtstatus.wvu.edu/api/%s/?format=json" %timestamp

# Get PRT JSON Data
response = urllib.urlopen(url)
data = json.load(response)

try:
	oldTimestamp = _get_last_row('monitor.csv')[2]
except IOError:
	print "monitor.csv is empty."

if oldTimestamp!=data['timestamp']:
	toCSV(data)
	print "New data detected for %s...\nUploading..." %time.ctime(int(data['timestamp']))
	print json.dumps(data, indent=4, sort_keys=True)
	tweetStatus(data)
else:
	print "Status has not changed since: %s" %time.ctime(int(oldTimestamp))

# ********************************** END **********************************

