'''
'''
from copy import deepcopy

import pluginMycelium.config as config



class Meal(object):
  '''
  Container of portions.
  
  A meal has states:
  - served (what can be eaten)
  - consumed (what was eaten)
  
  A meal is a varying len list of portions.
  It might be empty.
  It might not include portion on channel of automata that created it.
  
  A meal does NOT include portions of zero amount.
  
  TODO Optimization: subclass SingleChannelMeal with faster methods.
  '''
  
  def __init__(self, essentialPixelelID):
    self.portions = []
    self.essentialPixelelID = essentialPixelelID  # location of automata is eating
    self.essentialAmount = 0 # how much of essential channel was eaten
    
    
  def append(self, portion):
    assert portion.amount > 0, 'Portions should not be empty'
    self.portions.append(portion)
    
    # Remember if portion on essential pixelel is appended
    if portion.pixelelID == self.essentialPixelelID:
      self.essentialAmount = portion.amount
    
    
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
    Whether there are any portions.
    Since no portion may have zero amount, same as whether meal has any calories.
    
    !!! This does not guarantee there are calories in any particular pixelel of the meal.
    '''
    return len(self.portions) <= 0
  
  def isEssentiallyEmpty(self):
    ''' Whether meal ate the essential channel. '''
    return self.essentialAmount == 0
  
  
  def clamp(self):
    '''
    Change state of meal from served to consumed.
    Meal consumed, in range [0, mouth_size]
    I can only eat so much, and no more than is available.
    
    Might better be called chomp (or limit high).
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
    Copy of self with all portions AND essentialAmount clamped.
    '''
    result = deepcopy(self)
    for portion in result.portions:
      portion.amount = min(portion.amount, config.mealCalories)
      
    result.essentialAmount = min(result.essentialAmount, config.mealCalories)
    return result
  
  # TODO resolve portionCalories versus mealCalories
  
  
  def maxAmount(self):
    '''
    Max amount of meal in any single portion.
    Portions may be in different channels.
    Caller should not assume result is in any particular channel
    (or that it will add to any channel without overflow.)
    '''
    result = 0
    for portion in self.portions:
      if portion.amount > result:
        result = portion.amount
    return result
  
  
  def amount(self):
    '''
    Optimization.
    
    !!! Requires meal has a single portion, i.e. for SinglePixelMouth
    '''
    return self.portions[0].amount
  
  