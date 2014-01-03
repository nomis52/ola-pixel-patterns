#!/usr/bin/python
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# gameoflife.py
# Copyright (C) 2013 Simon Newton

import array
import math
import numpy

from ola.ClientWrapper import ClientWrapper

TICK_INTERVAL = 100  # in ms

class Pixel(object):
  def __init__(self, x, y, data, size=8):
    self._data = data
    self._offset = y * size
    if y % 2:
      self._offset += size - 1 - x
    else:
      self._offset += x
    self._offset *= 3

  def Red(self, i):
    self._data[self._offset] = i

  def Green(self, i):
    self._data[self._offset + 1] = i

  def Blue(self, i):
    self._data[self._offset + 2] = i


class Game(object):
  def __init__(self, size):
    self._size = size
    self.InitBoard(size)
    self._wrapper = ClientWrapper()
    self._data = array.array('B', [0] * (size * size * 3))
    self._pixels = [ self.GenList(y) for y in xrange(size) ]

  def InitBoard(self, size):
    def BoolToInit(b):
      if b:
        return 1
      else:
        return 0
    func = numpy.vectorize(BoolToInit)
    self._board = func(numpy.random.random((size, size)) > 0.75)

  def Run(self):
    self._wrapper.AddEvent(10, self.SendDMXFrame)
    self._wrapper.Run()

  def GenList(self, y):
    return [ Pixel(x, y, self._data) for x in xrange(self._size) ]

  def Evolve(self):
      alive = self._board > 0
      nbrs_count = sum(numpy.roll(numpy.roll(alive, i, 0), j, 1)
                       for i in (-1, 0, 1) for j in (-1, 0, 1)
                       if (i != 0 or j != 0))
      survive = (nbrs_count == 3) | (alive & (nbrs_count == 2))
      new = self._board * survive + survive
      return new

  def SetCell(self, pixel, age):
    if age >= 8:
      r = g = b = 255
    else:
      r = 255 * (age % 2)
      g = 255 * ((age >> 1) % 2)
      b = 255 * ((age >> 2) % 2)

    pixel.Red(r)
    pixel.Green(g)
    pixel.Blue(b)

  def SendDMXFrame(self):
    self._wrapper.AddEvent(TICK_INTERVAL, self.SendDMXFrame)

    for x in xrange(self._size):
      for y in xrange(self._size):
        self.SetCell(self._pixels[x][y], self._board[x][y])

    self._wrapper.Client().SendDmx(1, self._data)
    self._board = self.Evolve()


game = Game(8)
game.Run()
