'''

'''

from gimpfu import *


class AutomataSimulator(object):
  '''
  '''
  
  def __init__(self, frame, field):
    self.frame = frame
    self.field = field
    self.generationCount = 0
  
  
  def simulate(self):
    '''
    Simulation loop.
    Do simulate time periods until termination condition.
    '''
    # Python idiom for do until
    while True:
      self.generationCount += 1
      for automata in self.field.automataGenerator():
        automata.live()
        
      if self.field.isTerminal():
        break
      
      # TODO if animated
      self.flush()
      # TODO progress bar
      print(">>>>>>>>>>>>>>>>Generation ", self.generationCount)
        
        
  def flush(self):
    ''' Flush results to display. '''
    self.field.artifacts.flush()  # flush pixmap to Gimp image
    pdb.gimp_displays_flush() # displays become visible
  
  