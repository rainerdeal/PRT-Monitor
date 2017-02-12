# PRT Monitor v1.0
# by Ricky

import time, urllib, json, csv, os
from collections import deque
from twython import Twython
from auth import (
	consumer_key,
	consumer_secret,
	access_token_key,
	access_token_secret)

# Convert JSON to CSV and save it
def toCSV(data):

	if os.path.isfile('monitor.csv') == True:
		csvData = open('monitor.csv', 'a')
	
		# Create the CSV writer object
		csvWriter = csv.writer(csvData)

		csvWriter.writerow(data.values())
	else:
		csvData = open('monitor.csv', 'a')
	
		# Create the CSV writer object
		csvWriter = csv.writer(csvData)
	
		csvWriter.writerow(data.keys())
		csvWriter.writerow(data.values())
	
	csvData.close()

def get_last_row(csv_filename):
	with open(csv_filename, 'r') as f:
		try:
			lastrow = deque(csv.reader(f), 1)[0]
		except IndexError:  # empty file
			lastrow = None
		return lastrow

# Analyze monitor data. First attempt: just check for any status that does not = 1 
def scanCSV(csv_filename):
	downNumber = 0
	with open(csv_filename, 'r') as f:
		try:
			reader = csv.reader(f)
			next(reader)
			for r in reader:
				if r[0] != '1':
					downNumber+=1
				print(r[0])
		except IndexError: # empty file
			downNumber = 0
		return downNumber

def tweetStatus(data):
	Twitter = Twython(
		consumer_key,
		consumer_secret,
		access_token_key,
		access_token_secret)

	Twitter.update_status(status=data['message'])
	print(data['message'])
	
# ********************************* START *********************************
status = ""
message = ""
oldTimestamp = ""
timestamp = int(time.time())
url = "http://prtstatus.wvu.edu/api/%s/?format=json" %timestamp
	
# Get PRT JSON Data
response = urllib.urlopen(url)
data = json.load(response)

# Save Status and Message to variables for later use.
status = data['status']
message = data['message']

try:
	oldTimestamp = get_last_row('monitor.csv')[2]
except IOError:
	print "monitor.csv is empty."

if oldTimestamp!=data['timestamp']:
	toCSV(data)
	print "New data detected for %s...\nUploading..." %time.ctime(int(data['timestamp']))
	print json.dumps(data, indent=4, sort_keys=True)
	#tweetStatus(data)
else:
	print "Status has not changed since: %s" %time.ctime(int(oldTimestamp))

print("Number of times the PRT was not operating normally: %s" %scanCSV('monitor.csv'))
# ********************************** END **********************************
