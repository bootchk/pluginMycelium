'''
'''
from .mouth import Mouth
from pluginMycelium.meal.meal import Meal
from pluginMycelium.meal.portion import Portion



class SinglePixelMouth(Mouth):
  '''
  Mouth whose range is just one pixel.
  
  All meals have a single portion.
  '''
  
  def mealAt(self, automata):
    ''' Effect deferred method. '''
    meal = Meal()
    pixelelID = automata.pixelelID()
    amount = self.food.at(pixelelID)
    if amount > 0:
      portion = Portion(pixelelID, amount)
      meal.append(portion)
    # else meal is empty
    
    return meal

  
  def updateFoodAt(self, automata, mealAtMouth, mealConsumed):
    '''
    Effect deferred method.
    
    !!! Optimize: assert meal has exactly one portion
    '''
    remainingFood = mealAtMouth.amount() - mealConsumed.amount()
    
    ## Original code to assign whole pixel of one pixelel
    ## self.pixmap[pixelelID.coord] =  array('B', (remainingFood, ))
    
    self.food.set(automata.pixelelID(), remainingFood)
    
    