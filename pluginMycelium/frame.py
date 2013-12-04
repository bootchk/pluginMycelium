'''
'''
from pixmap.coord import Coord

class Frame(object):
  '''
  Coordinate frame.
  
  Responsibilities:
  - know width, height
  - clip
  - know center
  '''
  
  def __init__(self, width, height):
    self.width = width
    self.height = height
    
  def center(self):
    result = Coord(self.width/2, self.height/2)
    return result