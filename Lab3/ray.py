from mathlib import *
from sphere import *
from math import pi, tan
from materials import *

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)


class Raytracer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.background_color = BLACK
    self.light = None
    self.scene = []
    self.clear()

  def clear(self):
    self.pixels = [
      [self.background_color for x in range(self.width)]
      for y in range(self.height)
    ]

  def write(self, filename):
  	writebmp(filename, self.width, self.height, self.pixels)

  def display(self, filename='out.bmp'):
  	self.render()
  	self.write(filename)

  def point(self, x, y, c = None):
    try:
      self.pixels[y][x] = c or self.current_color
    except:
      pass

  def scene_intersect(self, orig, direction):
    zbuffer = float('inf')

    material = None
    intersect = None

    for obj in self.scene:
      hit = obj.ray_intersect(orig, direction)
      if hit is not None:
        if hit.distance < zbuffer:
          zbuffer = hit.distance
          material = obj.material
          intersect = hit

    return material, intersect

  def cast_ray(self, orig, direction):
    material, intersect = self.scene_intersect(orig, direction)

    if material is None:
      return self.background_color

    light_dir = norm(sub(self.light.position, intersect.point))
    light_distance = length(sub(self.light.position, intersect.point))

    offset_normal = mul(intersect.normal, 1.1) 
    shadow_orig = sub(intersect.point, offset_normal) if dot(light_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
    shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
    shadow_intensity = 0

    if shadow_material and length(sub(shadow_intersect.point, shadow_orig)) < light_distance:
      shadow_intensity = 0.9

    intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)

    reflection = reflect(light_dir, intersect.normal)
    specular_intensity = self.light.intensity * (
      max(0, -dot(reflection, direction))**material.spec
    )

    diffuse = material.diffuse * intensity * material.albedo[0]
    specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
    return diffuse + specular


  def render(self):
    alfa = int(pi/2)
    for y in range(self.height):
      for x in range(self.width):
        i =  (2*(x + 0.5)/self.width - 1)*self.width/self.height*tan(alfa/2)
        j =  (2*(y + 0.5)/self.height - 1 )*tan(alfa/2)
        direction = norm(V3(i, j, -1))
        self.pixels[y][x] = self.cast_ray(V3(0,0,0), direction)


r = Raytracer(1500, 1000)

r.light = Light(
  position=V3(0, 0, 5),
  intensity=1.3
)

r.background_color = WHITE

r.scene = [
    #Oso cafe
    Sphere(V3(1, -1, -5), 1, red)
]

r.display()