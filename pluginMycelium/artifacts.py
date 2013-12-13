'''
'''
from compositor import Compositor



class Artifacts(Compositor, object):
  '''
  A map of artifacts.
  Wraps a pixmap (value of pixel is the amount of artifacts.)
  
  See Food.
  '''
  
  def __init__(self, pixmap):
    self.pixmap = pixmap
    self.compose = self.dispatchComposeMethod()


  def flush(self):
    ''' Delegate '''
    self.pixmap.flushAll()
    
    
  def depositAt(self, pixelelID, amount):
    '''
    Deposit pixelel value at pixelelID using compose method.
    
    In this design, an automata may wander off the field.
    Note an automata off the field can't stay non-exhausted very long since there is no food: reserves will deplete.
    
    Whether the amount is from this period (pixel) or a previous period depends on the caller, not a concern here.
    '''
    # not assert amount > 0
    if not self.pixmap.isClipped(pixelelID.coord):
      self.compose(pixelelID, amount)
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
        print "Non-zero deposit off the field?"
      pass
    
    