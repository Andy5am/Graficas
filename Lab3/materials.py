from mathlib import *
from dataclasses import dataclass

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

class Light(object):
  def __init__(self, position=V3(0,0,0), intensity=1):
    self.position = position
    self.intensity = intensity

class Material(object):
  def __init__(self, diffuse=WHITE, albedo=(1, 0), spec=0):
    self.diffuse = diffuse
    self.albedo = albedo
    self.spec = spec

class Intersect(object):
  def __init__(self, distance, point, normal):
    self.distance = distance
    self.point = point
    self.normal = normal


#materiales
red = Material(diffuse=color(255, 0, 0), albedo=(0.9,  0.9), spec=13)
coffee = Material(diffuse=color(143, 59, 24), albedo=(0.9,  0.3), spec=7)
lightCoffee = Material(diffuse=color(230, 170, 135), albedo=(0.9,  0.9), spec=35)
black = Material(diffuse=color(0, 0, 0), albedo=(0.3,  0.3), spec=3)
green = Material(diffuse=color(130, 223, 36), albedo=(0.9,  0.9), spec=10)
iron = Material(diffuse=color(186, 186, 186), albedo=(1,  1), spec=50)
white = Material(diffuse=color(250, 250, 250), albedo=(0.9,  0.9), spec=35)
