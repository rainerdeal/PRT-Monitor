''' 
	PRT Analysis
	
	Weekly statistics calculated based on the data collected by PRT_Monitor
	Copyright 2017, Ricky Deal, All rights reserved.
'''

import csv, time
from twython import Twython
from auth import (
	consumer_key,
	consumer_secret,
	access_token_key,
	access_token_secret)

# Analyze monitor data. Check for any status that does not = 1, 6, or 7
# returns total number of times the PRT went down
def calcDownFrequency(csv_filename):
	downFrequency = 0
	with open(csv_filename, 'r') as f:
		try:
			reader = csv.reader(f)
			next(reader)
			for r in reader:
				if (r[0] != '1') and (r[0] != '6') and (r[0] != '7'): 
					downFrequency+=1
					#print(r[0])
		except IndexError: # empty file
			downFrequency = 0
		return downFrequency

# Analyze monitor data. Try to calculate total time PRT was down
def calcDownTime(csv_filename):
	totalDownTime = 0
	data = []

	# Save any entries that are not "closed" to list
	with open(csv_filename, 'r') as f:
		try:
			reader = csv.reader(f)
			next(reader)
			for r in reader:
				if (r[0]!='6') and (r[0]!='7'):
					data.append(r)
		except IndexError: # empty file
			print "monitor.csv is empty."

	# Calculate time
	downFlag = False
	lastDownTime = 0
	lastUpTime = 0
	for x in data:
		if downFlag==False and ((x[0]=='2') or (x[0]=='3') or (x[0]=='4') or (x[0]=='5') or (x[0]=='8')):
			downFlag = True
			lastDownTime = x[2]
		elif downFlag==True and x[0]=='1':
			downFlag = False
			lastUpTime = x[2]
			totalDownTime+=(int(lastUpTime)-int(lastDownTime))
	totalDownTime = (totalDownTime/60)/60
	return totalDownTime

# Analyze monitor data. Try to calculate total time PRT was up
def calcUpTime(csv_filename):
	totalUpTime = 0
	data = []

	# Save any entries that are not "closed" to list
	with open(csv_filename, 'r') as f:
		try:
			reader = csv.reader(f)
			next(reader)
			for r in reader:
				if (r[0]!='6') and (r[0]!='7'):
					data.append(r)
		except IndexError: # empty file
			print "monitor.csv is empty."

	# Calculate time
	upFlag = False
	lastUpTime = 0
	lastDownTime = 0
	
	for x in data:
		if upFlag==False and x[0]=='1':
			upFlag = True
			lastUpTime = x[2]
		elif upFlag==True and ((x[0]=='2') or (x[0]=='3') or (x[0]=='4') or (x[0]=='5') or (x[0]=='8')):
			upFlag = False
			lastDownTime = x[2]
			totalUpTime+=(int(lastDownTime)-int(lastUpTime))
	totalUpTime = (totalUpTime/60)/60
	return totalUpTime

# ********************************* START *********************************

Twitter = Twython(
	consumer_key,
	consumer_secret,
	access_token_key,
	access_token_secret)

#percentUpTime = float(calcUpTime('monitor.csv')/calcDownTime('monitor.csv'))

#message_f = ("Breakdowns: %s\nUptime: %s%" %(calcDownFrequency('monitor.csv'), percentUpTime))

#Twitter.update_status(status=message_f)
#print(percentUpTime)
print(float(calcUpTime('monitor.csv')/calcDownTime('monitor.csv')))

# ********************************** END **********************************

