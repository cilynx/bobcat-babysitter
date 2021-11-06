#!/usr/bin/env python

import time
from bobcat import Bobcat

bobcat = Bobcat('your bobcat ip')

sleep_mins = 5

print("Entering loop")
bobcat.last_gap = bobcat.gap

while True:
    print([getattr(bobcat, attr) for attr in ['timestamp','status','gap','miner_height','blockchain_height','ota_version','temp0','temp1','errors']])
    if bobcat.gap > 10 and bobcat.gap > bobcat.last_gap:
        bobcat.reset()
        bobcat.fastsync()
    bobcat.last_gap = bobcat.gap
    time.sleep(sleep_mins*60)
