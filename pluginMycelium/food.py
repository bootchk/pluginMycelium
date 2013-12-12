'''
'''

from mouth import SinglePixelMouth

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

    self.mouth = SinglePixelMouth(self)


  def eat(self, pixelelID):
    '''
    Try to eat.  Return what did eat.
    '''
    foodAtMouth = self.mouth.at(position=pixelelID)
    result = self.mouth.clamp(foodAtMouth)
    if result > 0:
      self.mouth.updateFoodAt(pixelelID, foodAt=foodAtMouth, consumed=result)
      self._eatenAmount += result
      ##print("Ate", result, " at ", pixelelID)
    return result
      
        
  def isAvailableAt(self, pixelelID):
    return self.at(pixelelID) > 0
  
  
  def at(self, pixelelID):
    ''' 
    Food at pixelelID when pixelelID may need clipping. 
    This is a sensor, not a mouth, i.e. what automata can sense, not what its mouth may get.
    '''
    if self.pixmap.isClipped(pixelelID.coord):
      result = 0
    else:
      result = self._foodAt(pixelelID)
    return result
  
  
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
  
    