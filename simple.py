#!/usr/bin/python

import array
from ola.ClientWrapper import ClientWrapper

wrapper = None
i = 0
TICK_INTERVAL = 20  # in ms

def SendDMXFrame():
  global i
  data = array.array('B', [i % 256, 0, 0] * 64)
  i += 1

  wrapper.Client().SendDmx(1, data)
  wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)

wrapper = ClientWrapper()
wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
wrapper.Run()
