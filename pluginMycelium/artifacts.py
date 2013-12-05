'''
'''
from array import array

class Artifacts(object):
  '''
  A map of artifacts.
  Wraps a grayscale pixmap (value of gray is the amount of artifacts.)
  
  See Food.
  '''
  
  def __init__(self, pixmap):
    self.pixmap = pixmap


  def depositAt(self, position, amount):
    '''
    In this design, an automata may wander off the field.
    So the poop here is from yesterday's meal (today's metabolism) even though we might not have eaten.
    Note an automata can't stay healthy very long off the field.
    '''
    if not self.pixmap.isClipped(position):
      ##print("depositAt", position)
      ##self.maximizeArtifact(position)
      self.incrementArtifact(position, amount)
    else:
      '''
      !!! A deposit off the field dissappears from view, but is not a RuntimeError
      raise RuntimeError, "Wandered off field, should not be metabolizing"
      '''
      print("Deposit off the field.")
      pass
    
  
  # ALTERNATIVE 1
  def incrementArtifact(self, position, amount):
    '''
    Artifacts analog, slowly build up as automatas metabolize.
    '''
    # Subtract: Gimp is a brightness 'value' where larger is whiter, subtract amount towards black.
    currentArtifact = self.pixmap[position][0]
    newArtifact = currentArtifact - amount
    if newArtifact < 0:
      newArtifact = 0 # clamp
    self.pixmap[position] = array('B', (newArtifact, ))
    
  
  # ALTERNATIVE 2
  def maximizeArtifact(self, position):
    '''
    Artifacts boolean: black 0 or white 255.
    '''
    self.pixmap[position] = array('B', (0, ))
    
    
  def flush(self):
    ''' Delegate '''
    self.pixmap.flushAll()