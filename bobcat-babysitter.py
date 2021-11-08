#!/usr/bin/python3 -u

import time
import pywemo
from bobcat import Bobcat

bobcat = Bobcat('your bobcat ip')
switch = pywemo.discovery.device_from_description('http://your-wemo-ip:49153/setup.xml')

sleep_mins = 5

print("Entering loop")
try:
    bobcat.last_gap = bobcat.gap
except:
    print("Bobcat is not responding.  Rebooting via smart plug.")
    switch.off()
    time.sleep(10)
    switch.on()
    bobcat.last_gap = bobcat.gap

count = 0
while True:
    try:
        print([getattr(bobcat, attr) for attr in ['timestamp','uptime','status','gap','miner_height','blockchain_height','ota_version','temp0','temp1','errors']])
        if status == "Down":
            if count == 3:
                print("Miner has been down for 3-cycles.  Rebooting via API.")
                bobcat.reboot()
            else:
                count += count
        else:
            count = 0
            if bobcat.gap > 10 and bobcat.gap > bobcat.last_gap:
                bobcat.reset()
                bobcat.fastsync()
            bobcat.last_gap = bobcat.gap
    except:
        print("Bobcat is not repsonding.  Rebooting via smart plug.")
        switch.off()
        time.sleep(10)
        switch.on()
    time.sleep(sleep_mins*60)
