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
	tweetStatus(data)
else:
	print "Status has not changed since: %s" %time.ctime(int(oldTimestamp))
# ********************************** END **********************************
