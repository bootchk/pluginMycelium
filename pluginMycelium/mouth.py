'''
'''

import config

class Mouth(object):
  '''
  Behaviour of automata interacting with food.
  
  This is a mouth whose range is just one pixel.
  '''
  
  def __init__(self, food):
    self.food = food  # mouth knows food
    
  
  def at(self, position):
    '''
    Food at mouth when mouth is at position.
    Might be greater than mouth can clamp.
    '''
    return self.food.at(position)
  
  
  def clamp(self, foodAtMouth):
    '''
    Food consumed, in range [0, mouth_size]
    I can only eat so much, and no more than is available.
    '''
    if foodAtMouth > config.mealCalories:
      result = config.mealCalories
    else:
      result = foodAtMouth
    assert result >= 0 and result <= config.mealCalories
    return result
  
  
  def updateFoodAt(self, pixelelID, foodAt, consumed):
    '''
    Consume food.
    Mouth knows the range of pixels it is consuming from.
    
    Note Pixmap does not support operand -= 
    Pixmap value is an array
    '''
    remainingFood = foodAt - consumed
    
    ## Original code to assign whole pixel of one pixelel
    ## self.pixmap[pixelelID.coord] =  array('B', (remainingFood, ))
    
    self.food.pixmap.setPixelel(pixelelID, remainingFood)
    
    