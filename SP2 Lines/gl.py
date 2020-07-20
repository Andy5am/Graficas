#Andy Castillo 18040
#SR1: Point

import struct

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(c):
  return struct.pack('=h', c)

def dword(c):
  return struct.pack('=l', c)

class Render(object):
  def __init__(self):
    self.framebuffer = []

  def glInit(self):
    self.width = 400
    self.height = 400

  def glCreateWindow(self, width, height):
    self.width = width
    self.height= height

  def glViewPort(self, x ,y , width, height):
    self.xVP = x
    self.yVP = y
    self.widthVP = width
    self.heightVP = height

  def glClear(self):
    self.framebuffer = [
      [self.backgroundColor for x in range(self.width)]
      for y in range(self.height)
    ]
    
  def glClearColor(self, r, g , b):
    self.backgroundColor = bytes([b*255, g*255, r*255])

  def glVertex(self, x , y):
    coordX = round(self.xVP + (self.widthVP/2 * (1+x)))
    coordY = round(self.yVP + (self.heightVP/2 * (1+y)))
    self.framebuffer[coordX][coordY] = self.color

  def glColor(self, r, g , b):
    self.color = bytes([b*255, g*255, r*255])

  def glFinish(self, filename):
    f = open(filename, 'bw')


    #file header
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    #image header
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    #pixel data

    for x in range(self.width):
      for y in range(self.height):
        f.write(self.framebuffer[y][x])

    f.close()

  def glLine(self, x0, y0, x1, y1):

    dy = abs(y1-y0)
    dx = abs(x1-x0)

    steep = dy > dx
    if steep:
      x0, y0 = y0, x0
      x1, y1 = y1, x1

    if x0 > x1:
      x0, x1 = x1, x0
      y0, y1 = y1, y0

    dy = abs(y1-y0)
    dx = abs(x1-x0)

    offset = 0
    threshold = dx

    y = y0
    x0 = int(x0*100)
    x1 = int(x1*100)

    inc = 1 if y1 > y0 else -1
    for x in range(x0, x1 + 1,):
      x = x/100
      if steep:
        self.glVertex(y, x)
      else:
        self.glVertex(x, y)

      offset += dy * 2
      if offset >= threshold:
        y += inc/100
        threshold += 2*dx

bitmap = Render()

bitmap.glCreateWindow(100, 100)
bitmap.glClearColor(0,0,0)
bitmap.glClear()
bitmap.glViewPort(0,0,50,50)
bitmap.glColor(0,0,1)
# bitmap.glVertex(0,0)
bitmap.glLine(1,1,-1,-1)
bitmap.glLine(1,-1,-1,1)
bitmap.glLine(-1,1,1,1)
bitmap.glLine(-1,-1,1,-1)
bitmap.glLine(-1,-1,-1,1)
bitmap.glLine(1,-1,1,1)
bitmap.glLine(0,-1,0,1)
bitmap.glLine(-1,0,1,0)
bitmap.glLine(-0.5,-1,0.5,1)
bitmap.glLine(0.5,-1,-0.5,1)
bitmap.glLine(-1,0.5,1,-0.5)
bitmap.glLine(-1,-0.5,1,0.5)
bitmap.glFinish('out.bmp')