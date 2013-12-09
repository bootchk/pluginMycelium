'''
'''

from array import array

import config



class Food(object):
  '''
  A map of food.
  Wraps a grayscale pixmap (value of gray is the amount of food.)
  '''
  
  def __init__(self, pixmap):
    self.pixmap = pixmap
    self._eatenAmount = 0
    
    # Count places that might have food
    self.places = pixmap.width * pixmap.height
    
    self._totalFood = self.totalFood()
    self._terminalEatenAmount = self._totalFood * config.terminationPercent / 100.0



  def eat(self, pixelelID):
    '''
    Try to eat.  Return what I did eat.
    '''
    if self.pixmap.isClipped(pixelelID.coord):
      result = 0
    else:
      result = self.whatICanEatAt(pixelelID)
      if result > 0:
        self.updateFoodAt(pixelelID, result)
        self._eatenAmount += result
        ##print("Ate", result, " at ", pixelelID)
    return result


  def whatICanEatAt(self, pixelelID):
    '''
    Food consumed, in range [0,GUT_SIZE]
    I can only eat so much, and no more than is available.
    '''
    # assert pixelelID is not clipped
    if self._foodAt(pixelelID) > config.mealCalories:
      result = config.mealCalories
    else:
      result = self._foodAt(pixelelID)
    assert result >= 0 and result <= config.mealCalories
    return result
      
        
  def isAvailableAt(self, pixelelID):
    if self.pixmap.isClipped(pixelelID.coord):
      result = False  # No food off the field
    else:
      result = self._foodAt(pixelelID) > 0
    return result
  
  
  def at(self, pixelelID):
    ''' Food at pixelelID when pixelelID may need clipping. '''
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
  
  
  def updateFoodAt(self, pixelelID, consumed):
    '''
    Consume food.  
    Note Pixmap does not support operand -= 
    Pixmap value is an array
    '''
    remainingFood = self._foodAt(pixelelID) - consumed
    
    ## Original code to assign whole pixel of one pixelel
    ## self.pixmap[pixelelID.coord] =  array('B', (remainingFood, ))
    
    self.pixmap.setPixelel(pixelelID, remainingFood)

    
    
  def totalFood(self):
    total = 0
    # Sum over pixels
    for pixel in self.pixmap:
      # Sum over pixelels of pixel
      for i in range(0, self.pixmap.bpp):
        total += pixel[i]
    return total
    
    
  def isMostlyGone(self):
    print("Eats", self._eatenAmount, "terminal", self._terminalEatenAmount)
    return self._eatenAmount > self._terminalEatenAmount
  
    ## TODO this is not guaranteed to terminate
    ## return self.eatenAmount > ( self.places * 1 )
  
  def eatenAmount(self):
    ''' How much food has been eaten by all automata, so far. '''
    return self._eatenAmount
  
    