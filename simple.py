#!/usr/bin/python

import array
from ola.ClientWrapper import ClientWrapper

wrapper = None
loop_count = 0
TICK_INTERVAL = 20  # in ms

def SendDMXFrame():
  global loop_count
  data = array.array('B', [loop_count % 256, 0, 0] * 64)
  loop_count += 1

  wrapper.Client().SendDmx(1, data)
  wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)

wrapper = ClientWrapper()
wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
wrapper.Run()
