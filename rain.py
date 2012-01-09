import numpy as np
import g3d2
import g3d2sim
import sys
from time import time, sleep

class Drop:
  def __init__(self, X, Y):
    self.X = X
    self.Y = Y
    self.posX = np.random.random()*(self.X-1)
    self.posY = np.random.random()*(self.Y-1) / 12.0
    self.speed = 0.0#2.0 + 15.0*np.random.random()
    self.accel = 5.0+40.0*np.random.random()

  def iterate(self, dt):
    self.speed = self.speed + self.accel * dt
    self.posY = self.posY + dt*self.speed
    return (np.round(self.posX), np.round(self.posY))

rate = 60.0     # Generation rate

if len(sys.argv) > 1:
  g = g3d2.g3d2(sys.argv[1])
else:
  g = g3d2sim.g3d2sim()

drops = []

t0 = time()
field = np.zeros((72, 32))
while True:
  t1 = time()
  dt = t1 - t0
  t0 = t1

  for drop in drops:
    drop.iterate(dt)

  drops[:] = [drop for drop in drops if drop.posY <= 31.0]

  # Potentially add a drop
  exp_cdf = 1.0 - np.exp(-rate*dt)
  if exp_cdf >= np.random.random():
    drops.append(Drop(72, 32))

  # Draw Drops
  for drop in drops:
    field[np.round(drop.posX), np.round(drop.posY)] = 1.0 / 18.0 * drop.speed

  # Fade field
  field[field>0] = field[field>0] - 0.04/field[field>0]
  field = np.maximum(field, 0.0)
  field = np.minimum(field, 1.0)

  # Convert and draw
  g.write_screen(np.array(field*15.0, dtype=np.uint8).transpose().flatten())


