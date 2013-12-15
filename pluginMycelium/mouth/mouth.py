'''
'''
''' Using Eiffel terminology: deferred and effective, for virtual and reimplemented. '''



class Mouth(object):
  '''
  Behaviour of automata interacting with food.
  
  Abstract base class.
  '''
  def __init__(self, food):
    self.food = food  # mouth knows food
  
  
  '''
  Clamping is responsibility of meal.
  '''
  
  '''
  Responsibility:
  - know the extent of mouth (how much food it reaches.)  Not the same as size.
  '''
  def mealAt(self, automata):
    '''
    Meal at mouth of automata (at current place.)
    Might be greater than mouth can clamp.
    
    Result meal may be empty of portions.  Any portions are non-zero amount.
    I.E. does not ensure 'not meal.isEmpty()'
    '''
    raise NotImplementedError, "Deferred"
  
  
  def updateFoodAt(self, automata, mealAtMouth, mealConsumed):
    '''
    Consume food.
    Mouth knows the range of pixels it is consuming from.
    mealConsumed also knows what pixelels are involved.
    
    mealAtMouth is a cached value of the food at the automata.
    '''
    raise NotImplementedError, "Deferred"
  

  