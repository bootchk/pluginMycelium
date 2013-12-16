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
    
    pixelelID = automata.pixelelID()
    meal = Meal(essentialPixelelID=pixelelID)
    amount = self.food.at(pixelelID)
    if amount > 0:
      portion = Portion(pixelelID, amount)
      meal.append(portion)
    # else meal is empty
    
    return meal

  
  def updateFoodAt(self, automata, mealConsumed):
    '''
    Effect deferred method.
    
    !!! Optimize: assert meal has exactly one portion
    '''
    pixelelID = automata.pixelelID()
    remainingFood = self.food.at(pixelelID) - mealConsumed.singlePortionAmount()
    self.food.set(pixelelID, remainingFood)
    
    