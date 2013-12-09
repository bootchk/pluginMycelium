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


  def depositAt(self, pixelelID, amount):
    '''
    In this design, an automata may wander off the field.
    Note an automata off the field can't stay non-exhausted very long since there is no food: reserves will deplete.
    
    Whether the amount is from this period (pixel) or a previous period depends on the caller, not a concern here.
    '''
    # not assert amount > 0
    if not self.pixmap.isClipped(pixelelID.coord):
      ##print("depositAt", pixelelID)
      ##self.maximizeArtifact(pixelelID)
      self.incrementArtifact(pixelelID, amount)
    else:
      '''
      !!! A deposit off the field dissappears from view, but is not a RuntimeError
      raise RuntimeError, "Wandered off field, should not be metabolizing"
      '''
      if amount > 0:
        '''
        For now, this should never happen (it might as well be an assertion) but for future use, allow this.
        
        With a non-toroidal field, we get many zero deposits off the field (wandered automata.)
        '''
        print("Non-zero deposit off the field?")
      pass
    
  
  # ALTERNATIVE 1
  def incrementArtifact(self, pixelelID, amount):
    '''
    Artifacts not binary, slowly build in value as automatas metabolize.
    '''
    # Subtract: Gimp is a brightness 'value' where larger is whiter, subtract amount towards black.
    currentArtifact = self.pixmap.getPixelel(pixelelID)
    newArtifact = currentArtifact - amount
    if newArtifact < 0:
      newArtifact = 0 # clamp
    self.pixmap.setPixelel(pixelelID, newArtifact)
    
    ## ORIGINAL FOR HARDCODED CHANNEL
    ## self.pixmap[position] = array('B', (newArtifact, ))
    
  
  # ALTERNATIVE 2
  def maximizeArtifact(self, pixelelID):
    '''
    Artifacts boolean: black 0 or white 255.
    '''
    self.pixmap.setPixelel(pixelelID, 0)
    
    ## ORIGINAL FOR HARDCODED CHANNEL
    ## self.pixmap[pixelelID] = array('B', (0, ))
    
    
  def flush(self):
    ''' Delegate '''
    self.pixmap.flushAll()
    
    