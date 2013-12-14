'''
'''

from mouth import Mouth


class BigMouth(Mouth):
  '''
  Mouth which eats from more than one pixelel, either wide or deep or both.
  
  All subclasses share updateFoodAt() but reimplement mealAt()
  '''

  
  def updateFoodAt(self, automata, mealAtMouth, mealConsumed):  # mealAtMouth is not used.
    '''
    Effect deferred method.
    
    Assert mealConsumed is already clamped to mealAtMouth.
    Assert mealConsumed and mealAtMouth have portions in the same order by PixelelID.
    '''
    '''
    TODO this is a concern of artifacts.
    Since we are also depositing it, and can't deposit more than 255 in one pixelel.
    This might change, if we deposit at more than one pixelel.
    '''
    #assert mealConsumed.size() <= 255
    
    # TODO iterator function
    # Iterate over mealConsumed (same as iterating over patch.)
    # assert meal has no empty portions
    for portion in mealConsumed.portions:
      pixelelID = portion.pixelelID
      # We could also get foodAt from corresponding portion of mealAtMouth
      foodAt = self.food.pixmap.getPixelel(pixelelID)
      # assert 0 < foodAt <= 255
      remainingFood = foodAt - portion.amount
      self.food.set(pixelelID, remainingFood)

  
  