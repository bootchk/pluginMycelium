'''
'''
from .mouth import Mouth
from pluginMycelium.meal import Meal
from pluginMycelium.portion import Portion



class SinglePixelMouth(Mouth):
  '''
  Mouth whose range is just one pixel.
  
  All meals have a single portion.
  '''
  
  def mealAt(self, automata):
    ''' Effect deferred method. '''
    pixelelID = automata.pixelelID()
    portion = Portion(pixelelID, self.food.at(pixelelID))
    meal = Meal()
    meal.append(portion)
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
    
    