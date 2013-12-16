'''
'''

import config


class Food(object):
  '''
  A map of food.
  Wraps a pixmap (value of pixelel is the amount of food.)
  '''
  
  def __init__(self, pixmap):
    self.pixmap = pixmap
    self._eatenAmount = 0
    
    # Count places that might have food
    self.places = pixmap.width * pixmap.height
    
    self._totalFood = self.totalFood()
    self._terminalEatenAmount = self._totalFood * config.terminationPercent / 100.0


  def eat(self, automata):
    '''
    Try to eat.  Return what did eat.
    '''
    mealAtMouth = automata.mouth.mealAt(automata)
    mealConsumed = mealAtMouth.clamp()
    '''
    Note we are eating even if deposit might deposit nothing: the tests of the meal might be different.
    Should we have a test: isDepositable() ?
    '''
    if not mealConsumed.isEssentiallyEmpty():
      automata.mouth.updateFoodAt(automata, mealAtMouth=mealAtMouth, mealConsumed=mealConsumed)
      self._eatenAmount += mealConsumed.size()
      ##print("Ate", result, " at ", pixelelID)
    return mealConsumed
      
        
  def isAvailableAt(self, pixelelID):
    '''
    Is non-zero value at pixelelID (in channel at pixel.)
    '''
    return self.at(pixelelID) > 0
  
  
  def at(self, pixelelID):
    '''
    Getter.
    
    Food at pixelelID when pixelelID may need clipping. 
    This is a sensor, not a mouth, i.e. what automata can sense, not what its mouth may get.
    '''
    if self.pixmap.isClipped(pixelelID.coord):
      result = 0
    else:
      result = self._foodAt(pixelelID)
    return result
  
  
  def set(self, pixelelID, amount):
    '''
    
    Note Pixmap does not support operand -=   Pixmap value is an array.
    i.e. self.pixmap[coord][0] -= 1 doesn't work.
    '''
    self.pixmap.setPixelel(pixelelID, amount)
    
    
  def _foodAt(self, pixelelID):
    ''' 
    Knows how to convert pixmap to food.
    Pixmap indexing returns an array.
    Grayscale has one pixelel 
    
    !!! Private, when we know not pixelelID.isClipped
    '''
    return self.pixmap.getPixelel(pixelelID)
  
    
  def totalFood(self):
    total = 0
    # Sum over pixels
    for pixel in self.pixmap:
      # Sum over pixelels of pixel
      for i in range(0, self.pixmap.bpp):
        total += pixel[i]
    return total
    
    
  def isMostlyGone(self):
    #print("Eats", self._eatenAmount, "terminal", self._terminalEatenAmount)
    return self._eatenAmount > self._terminalEatenAmount
  
    ## TODO this is not guaranteed to terminate
    ## return self.eatenAmount > ( self.places * 1 )
  
  
  def eatenAmount(self):
    ''' How much food has been eaten by all automata, so far. '''
    return self._eatenAmount
  
    