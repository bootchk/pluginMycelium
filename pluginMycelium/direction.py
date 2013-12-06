'''
'''
import random

from pixmap.coord import Coord

import config



class Direction(object):
  '''
  A direction a automata can move.
  Limited to 8 cardinal directions, to each adjacent pixel.
  
  Inconsequential orientation of axis: that x increases to right, y increases down.
  
  TODO: for Paterson's worms, only 6 directions.
  I.E. consider the grid triangularly connected.
  
  Responsibility:
  - know squirminess
  - tweak self: change self controlled by squirminess
  - fork self
  '''
  
  unitCoords = [Coord( 1,-1),  # NE
                Coord( 0,-1),  # N
                Coord(-1,-1),  # NW
                Coord(-1, 0),  # W
                Coord(-1, 1),  # SW
                Coord( 0, 1),  # S 
                Coord( 1, 1),  # SE
                Coord( 1, 0),  # E
                ]
  
  
  def __init__(self, cardinal=None):
    if cardinal is None:
      # initialize randomly
      self.index=random.randint(0,7)
    else:
      assert cardinal >= 0 and cardinal <=7
      self.index = cardinal
      
    # Precompute static squirminess of self
    self.squirminess = self.setSquirminessChoices()
  
  
  def tweak(self):
    ''' Change direction slightly, to next or previous. '''
    choice = random.choice(self.squirminess)
    self.index += choice
    self.index = self.index % 8 # modulo
  
  
  def setSquirminessChoices(self):
    '''
    Choices for turning.
    Dispatch on parameter.
    Static over life of automata.
    '''
    if config.squirminess == 0: # Relaxed, straight (no turn) is a choice
      result = [-1, 0, 1]
    elif config.squirminess == 1:
      result = [1, -1] # Curly, always turn, but slightly
    else:
      result = [-2, 0, 2] # Kinky, hard turn or straight
    # [-2, -1, 0, 1, 2]
    return result
    
    
  def unitCoordFor(self):
    ''' Direction's Coord, that can be added to another Coord. '''
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
  
  