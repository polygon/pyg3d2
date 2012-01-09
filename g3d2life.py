import life
import numpy as np
import g3d2
import g3d2sim
import sys
from time import sleep

rate = 10.0     # Frame rate (wished)
restart = 30.0  # Reinitialize after this amount of seconds

if len(sys.argv) > 1:
  g = g3d2.g3d2(sys.argv[1])
else:
  g = g3d2sim.g3d2sim()

l = life.Life()
l.randomize()

screen = np.zeros(np.shape(l.field), dtype=np.int8)
iters = 0

while True:
  sc_old = screen
  screen = np.maximum(0, screen / 2)
  screen[l.field > 0] = np.minimum(np.maximum(sc_old[l.field > 0] + 2, 8), 15)
  g.write_screen(screen.transpose().flatten())
  l.iterate()
  sleep(1 / rate)
  iters = iters + 1
  if iters >= rate*restart:
    for i in range(15, -1, -1):
      screen = np.maximum(0, screen / 2)
      screen[l.field > 0] = i
      l.iterate()
      g.write_screen(screen.transpose().flatten())
      sleep(1 / rate)
    sleep(0.9)
    l.randomize()
    iters = 0
