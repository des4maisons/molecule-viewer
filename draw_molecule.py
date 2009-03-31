from __future__ import division
class Atom:
  def __init__(self, x, y, z, id):
    self.coordinate = Coordinate(x,y,z)
    self.id = id

class Coordinate:
  def __init__(self, x,y,z):
    self.x, self.y, self.z = [x,y,z]

  def __mul__(self, const):
    return Coordinate(self.x*const, self.y*const, self.z*const)
  
  def __add__(self, coor):
    return Coordinate(self.x + coor.x, self.y + coor.y, self.z + coor.z)
  
  # regular dot product
  def dot(self, vector):
    return (self.x * vector.x + self.y * vector.y + self.z * vector.z)
  
  def length(self):
    from math import sqrt
    return sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))
  
  # project self onto 'onto'
  def project(self, onto):
    len = length(onto)
    scale_factor = dot(self, onto)/(len**2)
    return onto * scale_factor

  # flatten takes a tuple of coordinates, which when interpreted as vectors
  # beginning at (0,0,0), define a plane in 3-dim'l space
  def flatten(self, plane=None):
    if plane == None: #defaults to x-y plane
      plane = (Coordinate(1,0,0), Coordinate(0,1,0))
    proj0 = self.project(plane[0])
    proj1 = self.project(plane[1])
    return proj0 + proj1

class Molecule:
  def __init__(self, filename):
    atoms = []
    f = file(filename)
    for line in f:
      if line.startswith("ATOM"):
        parse_atom(line)
      elif line.startswith("CONNECT"):
        parse_connect(line)
      elif line.startswith("COMPOUND"):
        parse_author(line)
      elif line.startswith("TER"):
        pass
      elif line.startswith("END"):
        pass

  def parse_atom(self, str):
    type, seqnum, elt, one, x, y, z, who, cares = str.split(" ")
    atoms.append(Molecule(x,y,z,seqnum))
  def parse_connect(self, str):
    pass
  # dimensions is a tuple of the number of characters on x and y axis
  def draw(self, plane=None, dimensions=None):
    if dimensions == None:
      dimensions = (80,32)
    flattened = [a.flatten for a in self.atoms]
    x_max = max([coor[0] for coor in flattened])
    x_min = min([coor[0] for coor in flattened])
    y_max = max([coor[1] for coor in flattened])
    y_min = min([coor[1] for coor in flattened])
    x_delta = x_max - x_min
    y_delta = y_max - y_min
    # make everything fit in our dimensions while maintaining proportions
    scale_factor = min(dimensions[0]/x_delta, dimension[1]/y_delta)
    # shift to be in the 1st quadrant (positive coordinates) close to (0,0)
    x_shift = x_min*dimensions[0]
    y_shift = y_min*dimensions[1]
    view = []
    for i in range(dimensions[0]):
      view.append([])
      for j in range(dimensions[1]):
        view[i].append("`")
    from math import ciel
    for atom in atoms:
      x = atom.flatten[0]*scale_factor - x_shift
      y = atom.flatten[1]*scale_factor - y_shift
      view[floor(x), floor(y)] = atom.symbol
    show(view)

def show(view):
  for row in view:
    for column in row:
      print column

if __name__ == "__main__":
  import sys
  filename = sys.args[1]
  Molecule(filename).draw
