'''
'''
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
    
    
  def calories(self):
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
    Automata should only eat so much, and no more than is available.
    
    Might better be called chomp (or limit high).
    Responsibility:
    - know calories of mouth (how much each portion should be)
    
    !!! If we do clamp, return a copy.  Else return self.
    Assert a meal and its clamp are read only subsequently.
    '''
    if self.calories() > config.mealCalories:
      # total calories greater than clamp implies might exist some portion greater than clamp
      self._clampPortions()
    else:
      # total calories less than clamp implies all portions less than clamp
      pass
    # assert each portion: result >= 0 and result <= config.mealCalories

  
  
  def _clampPortions(self):
    '''
    Clamp all portions AND essentialAmount.
    '''
    for portion in self.portions:
      portion.amount = min(portion.amount, config.mealCalories)
      
    self.essentialAmount = min(self.essentialAmount, config.mealCalories)
  
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
  
  
  def singlePortionAmount(self):
    ''' Optimization for SinglePixelMouth. '''
    assert len(self.portions) == 1
    return self.portions[0].amount
  
  