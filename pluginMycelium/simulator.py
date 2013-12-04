'''

'''

from gimpfu import *


class CellularAutomataSimulator(object):
  '''
  '''
  
  def __init__(self, frame, field):
    self.frame = frame
    self.field = field
    self.generationCount = 0
  
  
  def simulate(self):
    '''
    Simulation loop.
    Simulate time periods until no cell is eating.
    '''
    while True: # simulation periods until no more food
      someCellEating = False
      self.generationCount += 1
      for cell in self.field.cellGenerator():
        cell.live()
        if cell.isEating():
          someCellEating = True
      if not someCellEating:
        break
      # TODO if animated
      self.flush()
      print(">>>>>>>>>>>>>>>>Generation ", self.generationCount)
        
        
  def flush(self):
    ''' Flush results to display. '''
    self.field.artifacts.flush()  # flush pixmap to Gimp image
    pdb.gimp_displays_flush() # displays become visible
  
  