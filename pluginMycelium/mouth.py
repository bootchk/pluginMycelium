'''
'''

import config

''' Using Eiffel terminology: deffered and effective. '''



class Mouth(object):
  '''
  Behaviour of automata interacting with food.
  
  Abstract base class.
  '''
  def __init__(self, food):
    self.food = food  # mouth knows food
  
  def clamp(self, foodAtMouth):
    '''
    Food consumed, in range [0, mouth_size]
    I can only eat so much, and no more than is available.
    
    Responsibility:
    - know size of mouth (how much food it will hold)
    '''
    if foodAtMouth > config.mealCalories:
      result = config.mealCalories
    else:
      result = foodAtMouth
    assert result >= 0 and result <= config.mealCalories
    return result
  
  '''
  Responsibility:
  - know the extent of mouth (how much food it reaches.)  Not the same as size.
  '''
  def at(self, position):
    raise NotImplementedError, "Deferred"
  
  def updateFoodAt(self, pixelelID, foodAt, consumed):
    raise NotImplementedError, "Deferred"
  
  

class SinglePixelMouth(Mouth):
  '''
  Behaviour of automata interacting with food.
  
  This is a mouth whose range is just one pixel.
  '''
  
  def at(self, position):
    '''
    Food at mouth when mouth is at position.
    Might be greater than mouth can clamp.
    
    Effect deferred method.
    '''
    return self.food.at(position)

  
  
  def updateFoodAt(self, pixelelID, foodAt, consumed):
    '''
    Consume food.
    Mouth knows the range of pixels it is consuming from.
    
    Effect deferred method.
    
    Note Pixmap does not support operand -= 
    Pixmap value is an array
    '''
    remainingFood = foodAt - consumed
    
    ## Original code to assign whole pixel of one pixelel
    ## self.pixmap[pixelelID.coord] =  array('B', (remainingFood, ))
    
    self.food.pixmap.setPixelel(pixelelID, remainingFood)
    
    