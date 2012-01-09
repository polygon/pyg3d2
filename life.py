import numpy as np
import pdb

class Life:
  def __init__(self, X=72, Y=32):
    self.X = X
    self.Y = Y
    self.field = np.zeros((self.X, self.Y), dtype=np.uint8)

  def randomize(self, prob=0.5):
    self.field = np.array(np.random.binomial(1, prob, np.shape(self.field)), dtype=np.uint8)

  def iterate(self):
    # Construct field that is "circular" around the edges
    cfield = np.zeros((self.X+2, self.Y+2), dtype=np.uint8)
    cfield[1:-1, 1:-1] = self.field
    cfield[0, 1:-1] = self.field[-1, :]
    cfield[-1, 1:-1] = self.field[0, :]
    cfield[1:-1, 0] = self.field[:, -1]
    cfield[1:-1, -1] = self.field[:, 0]
    cfield[0, 0] = self.field[-1, -1]
    cfield[-1, 0] = self.field[0, -1]
    cfield[0, -1] = self.field[-1, 0]
    cfield[-1, -1] = self.field[0, 0]

    neighbours = np.zeros((self.X, self.Y), dtype=np.uint8)
    neighbours = (cfield[0:-2, 0:-2] +
                  cfield[1:-1, 0:-2] +
                  cfield[2:, 0:-2] +
                  cfield[2:, 1:-1] +
                  cfield[2:, 2:] +
                  cfield[1:-1, 2:] +
                  cfield[0:-2, 2:] +
                  cfield[0:-2, 1:-1])

    self.field[neighbours == 3] = 1
    self.field[np.logical_or(neighbours < 2, neighbours > 3)] = 0
