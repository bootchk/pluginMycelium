'''
'''

from array import array

from config import GUT_SIZE as GUT_SIZE


class Food(object):
  '''
  A map of food.
  Wraps a grayscale pixmap (value of gray is the amount of food.)
  '''
  
  
  
  def __init__(self, pixmap):
    self.pixmap = pixmap


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
        print("Ate", result, " at ", position)
    return result


  def whatICanEatAt(self, position):
    '''
    Food consumed, in range [0,GUT_SIZE]
    I can only eat so much, and no more than is available.
    '''
    # assert position is not clipped
    if self.foodAt(position) > GUT_SIZE:
      result = GUT_SIZE
    else:
      result = self.foodAt(position)
    assert result >= 0 and result <= GUT_SIZE
    return result
      
        
  def isAvailableAt(self, position):
    if self.pixmap.isClipped(position):
      result = False  # No food off the field
    else:
      result = self.foodAt(position) > 0
    return result
  
  
  
  def foodAt(self, position):
    ''' 
    Knows how to convert pixmap to food.
    Pixmap indexing returns an array.
    Grayscale has one pixelel 
    '''
    return self.pixmap[position][0]
  
  def updateFoodAt(self, position, consumed):
    '''
    Consume food.  
    Note Pixmap does not support operand -= 
    Pixmap value is an array
    '''
    remainingFood = self.foodAt(position) - consumed
    self.pixmap[position] = array('B', (remainingFood, ))
    
    