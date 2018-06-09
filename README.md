# PRT-Monitor
Twitter bot 🤖 written in Python 🐍 that monitors WVU's PRT.

Copyright 2017, Ricky Deal, All rights reserved.
### Dependencies
* [Twython](https://github.com/ryanmcgrath/twython)
### Details:
Currently, I have PRT Monitor running on a [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) in headless mode. The scripts are triggered by [CRON](https://en.wikipedia.org/wiki/Cron) and I use a [Twitter App](https://apps.twitter.com) for the tweeting functionality. You can see PRT Monitor in action on [Twitter](https://twitter.com/PRTMonitor).

The PRT is currently undergoing a major rework. PRT "2.0" basically. It's a pretty big deal considering that it hasn't changed much since initial launch. They have been able to maintain ~95% uptime so far and hope to reach 99% with these upgrades. 🕵

Check out this cool historical snapshot of the PRT [here](http://www.boeing.com/history/products/personal-rapid-transit-system.page).

## What does it do?
### PRT_Monitor.py
Every 5 minutes this requests the PRT status from a JSON feed. If the status is different than the last status, then it will record the new status in a CSV file and tweet the new status.

So this doubles as both the twitter bot and the "monitor" at the same time.

### PRT_Analysis.py
This script is executed every Friday at 5pm. And here is what it does:

1. Adds up how many times the PRT has gone down during the semester.
2. Calculates the amount of time the PRT was out of service (doesn't include when the PRT is closed).
3. Calculates the amount of time the PRT was working normally.
4. Calculates the percentage of uptime.
5. Tweets the stats in a pretty format.

You're welcome to check my math (was never particularly good at it). 😬

### PRT_Prediction.py
This one is just an idea I had. It doesn't work yet. But I was thinking that I could predict outages based on historical data and weather.
