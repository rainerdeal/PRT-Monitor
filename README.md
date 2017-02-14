# PRT-Monitor
Bot written in Python that uses [Twython](https://github.com/ryanmcgrath/twython) and JSON to compile data on WVU's PRT Status.

## Details:
Currently, I have PRT Monitor running on a [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) in headless mode. 
The script was originally set up to run an infinite while loop that sleeps for 5 minutes. This turned out to be troublesome, becuase anytime I needed to move the RPI or change the script, I would have to reconnect it to a monitor, keyboard, and mouse becore I could get any work done on it. So I've set it up in headless mode and now use SSH and SCP to do any editing or checking up on how it's running. I replaced the infite while loop with [CRON](https://en.wikipedia.org/wiki/Cron) and scheduled PRT Monitor to run upon (re)boot and every 5 minutes.

PRT Monitor will gather the status information from the public JSON feed and save it to a CSV file so I can easily move it around, view it in a human-readable format, and parse it. The plan is to eventually scan this data periodically and tweet statistics about the PRT. 
I use a [Twitter App](https://apps.twitter.com) for the tweeting functionality. You can see PRT Monitor in action on [Twitter](https://twitter.com/PRTMonitor). 
