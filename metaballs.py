import numpy as np
import g3d2
import time

class Mbs:
  def __init__(self):
    self.X = 72
    self.Y = 32
    self.grid = np.meshgrid(range(self.X), range(self.Y))

  def rcosine(self, dist, strength, rolloff):
    res = 0.5 * (1.0 + np.cos(np.pi / (rolloff * strength) * (dist - (1.0 - rolloff) * strength / 2.0)))
    res[dist < (1.0-rolloff) * strength / 2.0] = 1.0
    res[dist > (1.0+rolloff) * strength / 2.0] = 0.0
    return res

  def build_field_march(self, mbs, edge0, edge1):
    field = np.zeros(np.shape(self.grid[0]))
    for mb in mbs:
      field = field + self.rcosine(np.sqrt(np.power(self.grid[0] - mb[0], 2) + np.power(self.grid[1] - mb[1], 2)), mb[2], mb[3])

    dfield = np.uint8(np.round(15.0 * (field - edge0) / (edge1 - edge0)))
    dfield[field < edge0] = 0
    dfield[field > edge1] = 15
#for x in range(72):
#      for y in range(32):
#        if field[x, y] < edge0:
#          dfield[x, y] = 0
#        elif field[x, y] > edge1:
#          dfield[x, y] = 15
#        else:
#          dfield[x, y] = np.uint8(np.round(15.0 * (field[x, y] - edge0) / (edge1 - edge0)))

    return dfield.transpose()

SPEED = 1.0
#N = 10
N = 60
tstart = time.time()
g = g3d2.g3d2('/dev/ttyUSB0')
m = Mbs()
mbs = np.zeros([N, 4])
#mbs[:, 2] = np.random.random([1, N]) * 4.0 + 8.0
mbs[:, 2] = np.random.random([1, N]) * 2.0 + 2.0
mbs[:, 3] = 1.0

fs = np.random.randn(N, 2) / 6

while True:
  t = time.time() - tstart
  mbs[:, 0:2] = (1.0+np.cos(2 * np.pi * fs * t)) * np.tile([36.0, 16.0], (N, 1))
  f = m.build_field_march(mbs, 0.0, 0.8)
  g.write_screen(list(f.transpose().flatten()))
