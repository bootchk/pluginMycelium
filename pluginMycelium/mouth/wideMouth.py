'''
'''

from pixmap.pixelelID import PixelelID

from .bigMouth import BigMouth
from pluginMycelium.meal.meal import Meal
from pluginMycelium.meal.portion import Portion



class WideMouth(BigMouth):
  '''
  Mouth whose range is pixels in a patch, i.e. neighborhood of adjacent pixels.
  In other words, mouth covers patch.
  Here, at() and update() iterate over patch.
  
  The patch shape depends on direction.swathCoords().
  Typically, three pixels, the pixel under the automata and two to the side (a swath).
  
  Pragmatically, a big mouth gives coarser grain, since an automata, by eating around itself,
  buffers itself from other automata, especially greedy automata.
  '''
  
  def _makePatch(self, automata):
    '''
    Container of PixelelID in a patch around automata.
    
    !!! cache for future call to updateFoodAt.
    ''' 
    patch = []
    swathCoords = automata.direction.swathCoords()
    for coord in swathCoords:
      wildPosition = automata.position + coord  # !!! wild, is unclipped
      if not self.food.pixmap.isClipped(wildPosition):
        patch.append(PixelelID(wildPosition, automata.pixelelIndex))
    # patch might be empty
    # Every PixelelID in patch has same PixelelIndex (channel)
    return patch
      
    
  def mealAt(self, automata):
    '''
    Effect deferred method.
    '''
    self.patch = self._makePatch(automata)
    
    meal = Meal(essentialPixelelID=automata.pixelelID())
    for pixelelID in self.patch:
      foodAt = self.food.at(pixelelID)
      if foodAt > 0:
        portion = Portion(pixelelID, foodAt)
        meal.append(portion)
    # meal may be empty of portions.  Any portions are non-zero amount
    '''
    meal.size() may be greater than 255 i.e. max pixelel value defined by graphics framework.
    assert that the caller will clamp it to 255 ???
    '''
    return meal

  
    
  """
  def clampValue(self, amount, clampValue):
    # Standard Python idiom for clamping in range [0, clampValue]
    return max(0, min(amount, clampValue))
  """
  
  