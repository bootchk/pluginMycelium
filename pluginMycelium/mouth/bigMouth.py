'''
'''

from .mouth import Mouth


class BigMouth(Mouth):
  '''
  Mouth which eats from more than one pixelel, either wide or deep or both.
  
  All subclasses share updateFoodAt() but reimplement mealAt()
  '''

  
  def updateFoodAt(self, automata, mealConsumed):
    '''
    Effect deferred method.
    
    Note automata not used: using PixelelID from portions.
    
    It is not a concern here whether mealConsumed.calories() <= 255.
    Assert for portion in meal: 0 < portion <= 255
    '''
    
    # Not the same as iterating over patch, since some of patch might not have a portion
    for portion in mealConsumed.portions:
      pixelelID = portion.pixelelID
      foodAt = self.food.at(pixelelID)
      # assert 0 <= foodAt <= 255
      remainingFood = foodAt - portion.amount
      # Writing to unsigned char, it will raise exception if math wrong, i.e. remainingFood < 0.
      self.food.set(pixelelID, remainingFood)

  
  