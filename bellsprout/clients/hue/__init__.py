from math import floor
from typing import Dict, List

from phue import Bridge
import time

#
# Hue does not run at a particular tick rate,  but ten messages per second is a comfortable place to work and you
# can talk about length of time in deciseconds to the bulb,  so let's do this for simplicity.
#
#

#
#
# Note: make simple instead of hard,  we are producing a wave form like
#
#
# [0,1,0]
#
# Our TICK is a multiple of deciseconds,  we will tell the lamp to ramp smoothly from one point to the
# other point assuming that we will send the next update on time.
#
#

message = dict(
   brightness = [1,254.0,1]
)

b = Bridge("192.168.0.30")

def play_message(light, message: Dict[str,List[float]],tick):
    lengths = {len(x) for x in message.values()}
    if len(lengths) !=1:
        raise Exception("Message must be a dict that contains one or more lists with the same length")

    last = {key: getattr(light,key) for key in message.keys()}
    length = list(lengths)[0]
    for i in range(0,length):
        then = time.time() + tick * 0.1
        for key in message.keys():
            value = floor(message[key][i])
            light.transitiontime=tick
            if last[key] != value:
                setattr(light, key, value)
                last[key] = value

        delay = then - time.time()
        time.sleep(delay)


#play_message(b.lights[4],message,5)