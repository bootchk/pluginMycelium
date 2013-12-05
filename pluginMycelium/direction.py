'''
'''
import random

from pixmap.coord import Coord

class Direction(object):
  '''
  A direction a automata can move.
  Limited to 8 cardinal directions, to each adjacent pixel.
  '''
  
  unitCoords = [Coord(1,1),  # NE
                Coord(0,1),  # N
                Coord(1,0),  # NW
                Coord(-1,0), # W
                Coord(-1,1), # SW
                Coord(0,-1),# S 
                Coord(-1,-1), # SE
                Coord(0,-1),  # E
                ]
  
  
  def __init__(self, cardinal=None):
    if cardinal is None:
      self.index=0
    else:
      assert cardinal >= 0 and cardinal <=7
      self.index = cardinal
  
  
  def tweak(self):
    ''' Change direction slightly, to next or previous. '''
    choice = random.choice([True, False])
    if choice:
      self.index += 1
    else:
      self.index -= 1
    self.index = self.index % 8 # modulo
  
  
  def unitCoordFor(self):
    ''' Coord to add to another Coord. '''
    return Direction.unitCoords[self.index]
  
  def setOpposite(self, other):
    ''' Set self opposite to other. '''
    self.index = other.index - 4
    self.index = self.index % 8
    
  def fork(self):
    ''' Two directions slightly left and right of self. '''
    leftIndex = (self.index - 1 ) % 8
    rightIndex = (self.index + 1 ) % 8
    return Direction(cardinal=leftIndex), Direction(cardinal=rightIndex)
  
  