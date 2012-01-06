import serial
import struct

class g3d2:

  def __init__(self, port):
    self.ser = serial.Serial(port, 500000)
    self.WIDTH = 9
    self.HEIGHT = 4

  def show_addr(self):
    self.ser.write('\x66\xfe')
    self.ser.flush()

  def write_pixel(self, x, y, intensity):
    modx = x / 8
    px = x % 8
    mody = y / 8
    py = y % 8

    module = self.WIDTH * (self.HEIGHT - mody - 1) + modx

    self.ser.write(struct.pack('BBBBB', 0x68, module, px, 7-py, intensity))
    self.ser.flush()

  def write_screen(self, data):
    # Data is expected to be a list with values between 0 to 15
    # The first 72 values correspond to the brightnesses of top LED row from left to right
    # The second 72 values correspond to the second row
    # In total, 32 rows are expected
    # Therefore it's a list with 2304 values

    self.ser.write('\x67')
    i = 0
    for mody in range(self.HEIGHT-1, -1, -1):
      for px in range(0, self.WIDTH*8):
        for py in range(7, -1, -2):
          y = mody*8 + py
          b0 = data[y*self.WIDTH*8 + px]
          b1 = data[(y-1)*self.WIDTH*8 + px]
          b = b0 + (b1 << 4)

          if b == 0x68:
            self.ser.write('\x65\x02')
          elif b == 0x67:
            self.ser.write('\x65\x01')
          elif b == 0x66:
            self.ser.write('\x65\x04')
          elif b == 0x65:
            self.ser.write('\x65\x03')
          else:
            self.ser.write(struct.pack('B', b))

    self.ser.write('\x00')
    self.ser.flush()
