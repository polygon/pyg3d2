import pygame
import threading
import sys
from time import time, sleep

class g3d2sim:
  def __init__(self, csize=14, cdist=2):
    self.csize = csize    # Size of circles
    self.cdist = cdist    # Distance between circles
    self.X = 72           # Wall width
    self.Y = 32           # Wall height
    self.t_screen = 0.025 # Time for screen update
    self.t_pixel = 0.0001 # Time for pixel update

    self.screen_width = self.X*csize + (self.X+1)*cdist
    self.screen_height = self.Y*csize + (self.Y+1)*cdist
    self.display_lock = threading.Lock()
    self.updater = threading.Thread(target=self.update)
    self.run = 1

    pygame.init()
    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
    self.updater.daemon = True
    self.updater.start()

  def update(self):
    while self.run==1:
      with self.display_lock:
        pygame.display.update()
      sleep(1/60.0)

  def draw_point(self, x, y, strength):
    if x < 0 or x >= self.X:
      return

    if y < 0 or y >= self.Y:
      return

    if strength < 0 or strength > 15:
      return

    pygame.draw.circle(self.screen,
                       (0, 255.0 / 15.0 * strength, 0),
                       ((self.csize+self.cdist)*x + self.csize/2+self.cdist, (self.csize+self.cdist)*y + self.csize/2+self.cdist),
                       self.csize/2
                      )

  def write_pixel(self, x, y, intensity):
    t0 = time()
    with self.display_lock:
      self.draw_point(x, y, intensity)
    t1 = time()
    if (t1-t0) < self.t_pixel:
      sleep(self.t_pixel - (t1 - t0))

  def write_screen(self, data):
    with self.display_lock:
      for idx, strength in enumerate(data):
        self.draw_point(idx % self.X, idx / self.X, strength)
      

  def exit(self):
    self.run = 0
    self.updater.join()
    pygame.quit()
