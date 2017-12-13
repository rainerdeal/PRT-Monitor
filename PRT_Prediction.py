"""	PRT Prediction
	
	Attempts to predict when PRT breakdowns are most likely to occur.
	Copyright 2017, Ricky Deal, All rights reserved.
"""

import csv, time, os, csv, pandas
from twython import Twython
from auth import (
	consumer_key,
	consumer_secret,
	access_token_key,
	access_token_secret)

""" Returns mondayDownFrequency, tuesdayDownFrequency, wednesdayDownFrequency, thursdayDownFrequency, fridayDownFrequency, saturdayDownFrequency
	
	Parse 'monitor.csv' and record any offline status.
	Returns total number of times the PRT went down for any week day.
""" 
def calcDownFrequencyByDay(csv_filename):
	
	(mondayDownFrequency, tuesdayDownFrequency, wednesdayDownFrequency, 
	thursdayDownFrequency, fridayDownFrequency, saturdayDownFrequency) = (0, 0, 0, 0, 0, 0)
	with open(csv_filename, 'r') as f:
		try:
			reader = csv.reader(f)
			next(reader)
			for r in reader:
				if (r[0] == '2') or (r[0] == '3') or (r[0] == '5') or (r[0] == '8'):
					if time.ctime(int(r[2])).startswith('Mon'):
						mondayDownFrequency+=1
					elif time.ctime(int(r[2])).startswith('Tue'):
						tuesdayDownFrequency+=1
					elif time.ctime(int(r[2])).startswith('Wed'):
						wednesdayDownFrequency+=1
					elif time.ctime(int(r[2])).startswith('Thu'):
						thursdayDownFrequency+=1
					elif time.ctime(int(r[2])).startswith('Fri'):
						fridayDownFrequency+=1
					elif time.ctime(int(r[2])).startswith('Sat'):
						saturdayDownFrequency+=1
		except IndexError: # empty file
			(mondayDownFrequency, tuesdayDownFrequency, wednesdayDownFrequency, 
			thursdayDownFrequency, fridayDownFrequency, saturdayDownFrequency) = (0, 0, 0, 0, 0, 0)
		return mondayDownFrequency, tuesdayDownFrequency, wednesdayDownFrequency, thursdayDownFrequency, fridayDownFrequency, saturdayDownFrequency

"""	Returns earlyDownFrequency, middayDownFrequency, afternoonDownFrequency, eveningDownFrequency
	
	Parse 'monitor.csv' and record and offline status.
	Returns total number of times the PRT went down for certain time intervals of ~4 hours.
"""
def calcDownFrequencyByTime(csv_filename):
	
	(earlyDownFrequency, middayDownFrequency, afternoonDownFrequency, eveningDownFrequency) = (0, 0, 0, 0)
	with open(csv_filename, 'r') as f:
		try:
			reader = csv.reader(f)
			next(reader)
			for r in reader:
				if (r[0] == '2') or (r[0] == '3') or (r[0] == '5') or (r[0] == '8'):
					rowSplit = time.ctime(int(r[2])).split(" ")
					justTime = rowSplit[-2].replace(':','')
					
					if int(justTime) <= (103000):			# Before 10:30am				(4 hours)
						earlyDownFrequency+=1
					elif 103000 < int(justTime) <= 143000:	# Between 10:30am and 2:30pm	(4 hours)
						middayDownFrequency+=1
					elif 143000 < int(justTime) <= 183000:	# Between 2:30pm and 6:30pm		(4 hours)
						afternoonDownFrequency+=1
					elif 183000 < int(justTime):			# After 6:30pm					(3.75 hours)
						eveningDownFrequency+=1
		except IndexError: # empty file
			(earlyDownFrequency, middayDownFrequency, afternoonDownFrequency, eveningDownFrequency) = (0, 0, 0, 0)
		return earlyDownFrequency, middayDownFrequency, afternoonDownFrequency, eveningDownFrequency

"""	Don't remember...
	
	This is why you comment your code... *sigh*
"""
def timeToCSV(csv_filename):
	
	data = ["filler"]
	with open(csv_filename, 'r') as f:
		reader = csv.reader(f)
		next(reader)
		for r in reader:
			if (r[0] == '2') or (r[0] == '3') or (r[0] == '5') or (r[0] == '8'):
				rowSplit = time.ctime(int(r[2])).split(" ")
				justTime = rowSplit[-2].replace(':','')
				data.append(justTime)
				
	# if CSV file exists then just write to it
	if os.path.isfile('downTime.csv') == True:	
		csvData = open('downTime.csv', 'a')
		csvWriter = csv.writer(csvData)	# Create the CSV writer object
		csvWriter.writerow(data)
	
	# else create the CSV file first, then write to it
	else:
		csvData = open('downTime.csv', 'a')
		csvWriter = csv.writer(csvData)	# Create the CSV writer object
		csvWriter.writerow("TIME")
		csvWriter.writerow(data)
	csvData.close()

# ********************************* START *********************************

Twitter = Twython(
	consumer_key,
	consumer_secret,
	access_token_key,
	access_token_secret)

message = ("The PRT has gone down %s times on Monday."
		 "\nThe PRT has gone down %s times on Tuesday."
		 "\nThe PRT has gone down %s times on Wednesday."
		 "\nThe PRT has gone down %s times on Thursday."
		 "\nThe PRT has gone down %s times on Friday." 
		 "\nThe PRT has gone down %s times on Saturday." %calcDownFrequencyByDay('monitor.csv'))

message2 = ("The PRT has gone down %s times before 10:30am."
		  "\nThe PRT has gone down %s times between 10:30am and 2:30pm."
		  "\nThe PRT has gone down %s times between 2:30pm and 6:30pm."
		  "\nThe PRT has gone down %s times after 6:30pm." %calcDownFrequencyByTime('monitor.csv'))

#Twitter.update_status(status=message_f)
print(message)
print""
print(message2)

#timeToCSV('monitor.csv')

# ********************************** END **********************************

