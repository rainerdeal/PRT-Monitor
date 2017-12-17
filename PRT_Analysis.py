# -*- coding: utf-8 -*-
""" PRT Analysis
    
    Weekly statistics calculated based on the data collected by PRT_Monitor
    Copyright 2017, Ricky Deal, All rights reserved.
"""

import csv, time
from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token_key,
    access_token_secret)

""" Returns downFrequency
    
    Parse 'monitor.csv' and find all entries that are not Normal(1) or Closed(6 & 7)
"""
def down_frequency(csv_filename):
    
    downFrequency = 0
    with open(csv_filename, 'r') as f:
        try:
            reader = csv.reader(f)
            next(reader)
            for r in reader:
                if (r[0] != '1') and (r[0] != '6') and (r[0] != '7'):
                    downFrequency+=1
        except IndexError: # empty file
            downFrequency = 0
        return downFrequency

""" Returns totalDownTime
    
    Parse 'monitor.csv' and find total time PRT was out of service.
"""
def down_time(csv_filename):
    
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

""" Returns totalUpTime
    
    Parse 'monitor.csv' and find total time PRT was in service.
"""
def up_time(csv_filename):
    
    totalUpTime = 0
    data = []

    # Save any entries that are not "closed" to list
    with open(csv_filename, 'r') as f:
        try:
            reader = csv.reader(f)
            next(reader)
            for r in reader:
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
        elif upFlag==True and ((x[0]=='2') or (x[0]=='3') or (x[0]=='4') or (x[0]=='5') or (x[0]=='6') or (x[0]=='7') or (x[0]=='8')):
            upFlag = False
            lastDownTime = x[2]
            totalUpTime+=(int(lastDownTime)-int(lastUpTime))
    totalUpTime = (totalUpTime/60)/60
    return totalUpTime

""" Returns percentUpTime
    
    Calculate percentage of time the PRT was operating normally
    (note: does not include hours the PRT was Closed.)
"""
def percent_up_time(totalUpTime, totalDownTime):

    totalTime = float(totalUpTime+totalDownTime)
    percentUpTime = (totalUpTime/totalTime)*100
    return round(percentUpTime, 2)

# ********************************* START *********************************

Twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token_key,
    access_token_secret)

downFrequency = down_frequency('monitor.csv')
upTime = up_time('monitor.csv')
downTime = down_time('monitor.csv')
percentUpTime = percent_up_time(upTime, downTime)

at = "@WVUDOT @gordongee"
part0 = "\n🌟🌟🌟🌟 PRT Stats 🌟🌟🌟🌟"
part1 = "\n  Breakdowns: %sx\n  Uptime:    %s%%" %(downFrequency, percentUpTime)
part2 = "\n#wvuprt #wvu #prt #📊"

message_f = (part0 + part1 + part2 + at)
#print(message_f)
Twitter.update_status(status=message_f)

# ********************************** END **********************************

