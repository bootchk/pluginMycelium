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


  def depositAt(self, position):
    '''
    '''
    if not self.pixmap.isClipped(position):
      self.maximizeArtifact(position)
    else:
      raise RuntimeError, "Wandered off field, should not be metabolizing"
    
    
  def incrementArtifact(self, position):
    '''
    Artifacts analog, slowly build up as automatas metabolize.
    '''
    # Decrement by 1: Gimp is a brightness 'value' where larger is whiter
    currentArtifact = self.pixmap[position][0]
    newArtifact = currentArtifact - 1
    if newArtifact < 0:
      newArtifact = 0 # clamp
    self.pixmap[position] = array('B', (newArtifact, ))
    
    
  def maximizeArtifact(self, position):
    '''
    Artifacts boolean: black 0 or white 255.
    '''
    self.pixmap[position] = array('B', (0, ))
    
    
  def flush(self):
    ''' Delegate '''
    self.pixmap.flushAll()