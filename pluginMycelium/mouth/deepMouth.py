'''
'''


from .bigMouth import BigMouth
from pluginMycelium.meal.meal import Meal
from pluginMycelium.meal.portion import Portion


class DeepMouth(BigMouth):
  '''
  Mouth whose range is one pixel but that covers all pixelels of pixel.
  Here, at() and update() iterate over pixelels.
  
  Pragmatically, a deep mouth doesn't alter hue, since its trail is same as original hue.
  But it might alter pattern, since by eating all pixelels,
  it buffers itself from other automata on other channels, 
  especially greedy automata that might turn away if this automata already ate the channel.
  '''
      
    
  def mealAt(self, automata):
    '''
    Effect deferred method.
    '''
    meal = Meal()
    for pixelelID in self.food.pixmap.pixelelIDsAt(automata.position):
      foodAt = self.food.at(pixelelID)
      if foodAt > 0:
        portion = Portion(pixelelID, foodAt)
        meal.append(portion)
    # meal may be empty of portions.  All portions are non-zero amount
    '''
    meal.size() may be greater than 255 i.e. max pixelel value defined by graphics framework.
    assert that the caller will clamp it to 255 ???
    '''
    return meal


  
  