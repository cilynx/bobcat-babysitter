#!/usr/bin/python3 -u

import time
#import pywemo
from pybobcat import Bobcat
from pytasmota import Tasmota

bobcat = Bobcat('your bobcat ip')
switch = Tasmota('your tasmota switch ip',your_outlet_id)
#switch = pywemo.discovery.device_from_description('http://your-wemo-ip:49153/setup.xml')

sleep_mins = 5

print("Setting up")
try:
    bobcat.last_height = bobcat.miner_height
except Exception as e:
    print(f"{e}  Rebooting via smart plug.")
    switch.off()
    time.sleep(10)
    switch.on()
    bobcat.last_height = bobcat.miner_height

time.sleep(sleep_mins*60)

print("Entering loop")
count = 0
while True:
    try:
        print([
            bobcat.timestamp,
            bobcat.uptime,
            bobcat.status,
            bobcat.gap,
            bobcat.miner_height,
            bobcat.blockchain_height,
            bobcat.ota_version,
            bobcat.miner["Image"],
            bobcat.temp0,
            bobcat.temp1,
            bobcat.errors
        ])
        if bobcat.status == "Down":
            if count == 3:
                print("Miner has been down for 3-cycles.  Rebooting via API.")
                bobcat.reboot()
            else:
                count += count
        elif bobcat.status == "Helium API Timeout":
            print("Helium API is having issues -- nothing we can do.  Waiting it out.")
        else:
            count = 0
            if isinstance(bobcat.last_height, int) and isinstance(bobcat.miner_height, int) and isinstance(bobcat.gap, int):
                if bobcat.gap > 10 and bobcat.miner_height == bobcat.last_height:
                    print("Gap is >10 and growing.")
                    bobcat.reset()
                    bobcat.fastsync()
            bobcat.last_height = bobcat.miner_height
    except Exception as e:
        print(f"{e}  Rebooting via smart plug.")
        switch.off()
        time.sleep(10)
        switch.on()
    time.sleep(sleep_mins*60)
