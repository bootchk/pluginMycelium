'''
'''
from copy import deepcopy

import config


class Meal(object):
  '''
  Container of portions.
  
  A meal has states:
  - served (what can be eaten)
  - consumed (what was eaten)
  
  TODO Optimization: subclass SingleChannelMeal with faster methods.
  '''
  
  def __init__(self):
    self.portions = []
    
    
  def append(self, portion):
    self.portions.append(portion)
    
    
  def size(self):
    '''
    Total calories (pixelel values) in the meal.
    '''
    result = 0
    for portion in self.portions:
      result += portion.amount
    return result
  
  
  def isEmpty(self):
    '''
    Whether any portions have calories (not whether there are any portions.)
    '''
    return self.size() <= 0
  
  
  def clamp(self):
    '''
    Meal consumed, in range [0, mouth_size]
    I can only eat so much, and no more than is available.
    
    Responsibility:
    - know size of mouth (how much food it will hold)
    
    !!! If we do clamp, return a copy.  Else return self.
    Assert a meal and its clamp are read only subsequently.
    '''
    if self.size() > config.mealCalories:
      # total size greater than clamp implies might exist some portion greater than clamp
      result = self._clampPortions()
    else:
      # total size less than clamp implies all portions less than clamp
      result = self
    # assert each portion: result >= 0 and result <= config.mealCalories
    return result
  
  
  def _clampPortions(self):
    '''
    Copy of self with all portions clamped.
    '''
    result = deepcopy(self)
    for portion in result.portions:
      portion.amount = min(portion.amount, config.mealCalories)
    return result
  
  # TODO resolve portionCalories versus mealCalories
  
  
  def maxAmount(self):
    '''
    Max amount of meal in any single portion (channel).
    '''
    result = 0
    for portion in self.portions:
      if portion.amount > result:
        result = portion.amount
    return result
  
  
  def amount(self):
    '''
    !!! Require meal has a portion, i.e. for SinglePixelMouth
    '''
    return self.portions[0].amount
  
  