from __future__ import division
class Coordinate2D(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def __mul__(self, const):
    return Coordinate2D(self.x * const, self.y * const)
  def __add__(self, coor):
    return Coordinate2D(self.x + coor.x, self.y + coor.y)
  def __sub__(self, coor):
    return self + coor * (-1)

class Atom(object):
  def __init__(self, x, y, z, symbol, id):
    self.coordinate = Coordinate(x,y,z)
    self.symbol = symbol
    self.id = id
  def flatten(self, plane=None):
    return self.coordinate.flatten(plane)

class Coordinate(object):
  def __init__(self, x,y,z):
    self.x, self.y, self.z = [x,y,z]
  
  def __repr__(self):
    return str((self.x, self.y, self.z))

  def __str__(self):
    return self.__repr__()

  def __truediv__(self, const):
    return self * (1/const)

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
    len = onto.length()
    scale_factor = self.dot(onto)/(len**2)
    return onto * scale_factor
  
  # cross product
  def cross(self, vector):
    a1, a2, a3 = [self.x, self.y, self.z]
    b1, b2, b3 = [vector.x, vector.y, vector.z]
    return Coordinate(a2 * b3 - a3 * b2,
                      a3 * b1 - a1 * b3,
                      a1 * b2 - a2 * b1)

  # flatten takes a 2-element list of coordinates. When interpreted as vectors,
  # these define a plane in 3-dim'l space
  def flatten(self, plane=None):
    if plane == None: #defaults to x-y plane
      plane = [Coordinate(1,0,0), Coordinate(0,1,0)]
    # get 2 perpendicular vectors that define the same plane
    perp = plane[0].cross(plane[1])
    plane[0] = perp.cross(plane[1])
    # make them unit vectors
    plane[0] = plane[0]/(plane[0].length())
    plane[1] = plane[1]/(plane[1].length())

    proj0 = self.project(plane[0])
    proj1 = self.project(plane[1])
    ratio0 = 0
    ratio1 = 0

    # the (signed) number of times the unit vector fits into the projection
    # is the 2 dimensional coordinate we want
    # so (2,0) == 2 * (1,0), 2 is what we want. don't divide by zero.
    for component in ["x", "y", "z"]:
      val = getattr(plane[0], component)
      if val != 0:
        ratio0 = getattr(proj0, component) / val
      val = getattr(plane[1], component)
      if val != 0:
        ratio1 = getattr(proj1, component) / val
    if not (ratio0 or ratio1): # if either are 0
      raise "plane defined with zero vector"
    return Coordinate2D(ratio0, ratio1)

class Molecule(object):
  def __init__(self, filename):
    self.atoms = []
    f = file(filename)
    for line in f:
      if line.startswith("ATOM"):
        self.parse_atom(line)
      elif line.startswith("CONNECT"):
        self.parse_connect(line)
      elif line.startswith("COMPOUND"):
        pass #self.parse_author(line)
      elif line.startswith("TER"):
        pass
      elif line.startswith("END"):
        pass
      elif line.startswith("AUTHOR"):
        pass
    else:
        pass

  def parse_atom(self, str):
    type, seqnum, elt, one, x, y, z, who, cares = str.split()
    self.atoms.append(Atom(float(x),float(y),float(z),elt,int(seqnum)))
  def parse_connect(self, str):
    pass
  # dimensions is Coordinate2D of the number of characters on x and y axis
  def draw(self, plane=None, dimensions=None):
    if dimensions == None:
      dimensions = Coordinate2D(80, 32)
    flattened = [a.flatten(plane) for a in self.atoms]
    max_extreme = Coordinate2D(max([coor.x for coor in flattened]),
                               max([coor.y for coor in flattened]))
    min_extreme = Coordinate2D(min([coor.x for coor in flattened]),
                               min([coor.y for coor in flattened]))
    delta = max_extreme - min_extreme
    # make everything fit in our dimensions while maintaining proportions
    scale_factor = min(dimensions.x/delta.x, dimension.y/delta.y)
    # shift to be in the 1st quadrant (positive coordinates) close to (0,0)
    shift = Coordinate2D(min.x * dimensions.x, min.y * dimensions.y)
    
    view = []
    for i in range(dimensions[0]):
      view.append([])
      for j in range(dimensions[1]):
        view[i].append("`")
    from math import ciel
    for atom in self.atoms:
      viewcoor = atom.flatten() * scale_factor - shift
      view[floor(viewcoor.x), floor(viewcoor.y)] = atom.symbol
    show(view)

def show(view):
  for row in view:
    for column in row:
      print column

if __name__ == "__main__":
  import sys
  filename = sys.argv[1]
  Molecule(filename).draw()
