'''
'''
from mouth import Mouth
from pixmap.pixelelID import PixelelID
from meal import Meal
from portion import Portion


class BigMouth(Mouth):
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
      if self.food.pixmap.isClipped(wildPosition):
        continue
      patch.append(PixelelID(wildPosition, automata.pixelelIndex))
    # patch might be empty
    return patch
      
    
  def mealAt(self, automata):
    '''
    Effect deferred method.
    '''
    self.patch = self._makePatch(automata)
    
    meal = Meal()
    for pixelelID in self.patch:
      foodAt = self.food.at(pixelelID)
      if foodAt > 0:
        portion = Portion(pixelelID, foodAt)
        meal.append(portion)
    # meal may not have any portions.  All portions are non-zero amount
    '''
    meal.size() may be greater than 255 i.e. max pixelel value defined by graphics framework.
    assert that the caller will clamp it to 255 ???
    '''
    return meal

  
  def updateFoodAt(self, automata, mealAtMouth, mealConsumed):  # foodAt is not used.
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

  
  """
  CRUFT
  def updateFoodAt(self, automata, mealAtMouth, mealConsumed):  # foodAt is not used.
    '''
    Effect deferred method.
    
    Here we eat the maximum at each pixel until we reach food consumed.
    So we may not eat from every pixel.
    The order of the patch makes a difference: for now, the center pixel is first.
    '''
    '''
    Since we are also depositing it, and can't deposit more than 255 in one pixelel.
    This might change, if we deposit at more than one pixelel.
    '''
    assert mealConsumed.size() <= 255
    
    yetToConsume = consumed
    
    for pixelelID in self.patch:
      foodAt = self.food.pixmap.getPixelel(pixelelID)
      if foodAt <= 0:
        continue
      # assert 0 < foodAt <= 255
      # Don't eat more from this pixel than ToConsume
      clamped = min(foodAt, yetToConsume)
      remainingFood = foodAt - clamped
      self.food.set(pixelelID, remainingFood)
      yetToConsume -= clamped
      if yetToConsume <= 0:
        break
  """
    
  """
  def clampValue(self, amount, clampValue):
    # Standard Python idiom for clamping in range [0, clampValue]
    return max(0, min(amount, clampValue))
  """
  
  