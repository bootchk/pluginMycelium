'''
'''

from array import array

import config
# from config import GUT_SIZE as GUT_SIZE


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



  def eat(self, position):
    '''
    Try to eat.  Return what I did eat.
    '''
    if self.pixmap.isClipped(position):
      result = 0
    else:
      result = self.whatICanEatAt(position)
      if result > 0:
        self.updateFoodAt(position, result)
        self._eatenAmount += result
        ##print("Ate", result, " at ", position)
    return result


  def whatICanEatAt(self, position):
    '''
    Food consumed, in range [0,GUT_SIZE]
    I can only eat so much, and no more than is available.
    '''
    # assert position is not clipped
    if self._foodAt(position) > config.mealCalories:
      result = config.mealCalories
    else:
      result = self._foodAt(position)
    assert result >= 0 and result <= config.mealCalories
    return result
      
        
  def isAvailableAt(self, position):
    if self.pixmap.isClipped(position):
      result = False  # No food off the field
    else:
      result = self._foodAt(position) > 0
    return result
  
  
  def at(self, position):
    ''' Food at position when position may need clipping. '''
    if self.pixmap.isClipped(position):
      result = 0
    else:
      result = self._foodAt(position)
    return result
  
  
  def _foodAt(self, position):
    ''' 
    Knows how to convert pixmap to food.
    Pixmap indexing returns an array.
    Grayscale has one pixelel 
    
    !!! Private, when we know not position.isClipped
    '''
    return self.pixmap[position][0]
  
  
  def updateFoodAt(self, position, consumed):
    '''
    Consume food.  
    Note Pixmap does not support operand -= 
    Pixmap value is an array
    '''
    remainingFood = self._foodAt(position) - consumed
    self.pixmap[position] = array('B', (remainingFood, ))
    
    
  def totalFood(self):
    total = 0
    for pixel in self.pixmap:
      total += pixel[0]   # Grayscale
    return total
    
    
  def isMostlyGone(self):
    print("Eats", self._eatenAmount, "terminal", self._terminalEatenAmount)
    return self._eatenAmount > self._terminalEatenAmount
  
    ## TODO this is not guaranteed to terminate
    ## return self.eatenAmount > ( self.places * 1 )
  
  def eatenAmount(self):
    ''' How much food has been eaten by all automata, so far. '''
    return self._eatenAmount
  
    