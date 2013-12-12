'''
'''

import config

from pixmap.pixelelID import PixelelID

''' Using Eiffel terminology: deffered and effective. '''



class Mouth(object):
  '''
  Behaviour of automata interacting with food.
  
  Abstract base class.
  '''
  def __init__(self, food):
    self.food = food  # mouth knows food
  
  def clamp(self, foodAtMouth):
    '''
    Food consumed, in range [0, mouth_size]
    I can only eat so much, and no more than is available.
    
    Responsibility:
    - know size of mouth (how much food it will hold)
    '''
    if foodAtMouth > config.mealCalories:
      result = config.mealCalories
    else:
      result = foodAtMouth
    assert result >= 0 and result <= config.mealCalories
    return result
  
  '''
  Responsibility:
  - know the extent of mouth (how much food it reaches.)  Not the same as size.
  '''
  def at(self, automata):
    '''
    Food at mouth of automata (at current place.)
    Might be greater than mouth can clamp.
    '''
    raise NotImplementedError, "Deferred"
  
  
  def updateFoodAt(self, automata, foodAt, consumed):
    '''
    Consume food.
    Mouth knows the range of pixels it is consuming from.
    
    foodAt is a cached value of the food at the automata.
    '''
    raise NotImplementedError, "Deferred"
  
  


class SinglePixelMouth(Mouth):
  '''
  Mouth whose range is just one pixel.
  '''
  
  def at(self, automata):
    ''' Effect deferred method. '''
    return self.food.at(automata.pixelelID())

  
  
  def updateFoodAt(self, automata, foodAt, consumed):
    '''
    Effect deferred method.
    
    Note Pixmap does not support operand -= 
    Pixmap value is an array
    '''
    remainingFood = foodAt - consumed
    
    ## Original code to assign whole pixel of one pixelel
    ## self.pixmap[pixelelID.coord] =  array('B', (remainingFood, ))
    
    self.food.pixmap.setPixelel(automata.pixelelID(), remainingFood)
    


class BigMouth(Mouth):
  '''
  Mouth whose range is pixels in a patch, i.e. neighboorhood of adjacent pixels.
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
      
    
  def at(self, automata):
    '''
    Effect deferred method.
    '''
    self.patch = self._makePatch(automata)
    
    result = 0
    for pixelelID in self.patch:
      result += self.food.at(pixelelID)
    '''
    result may be greater than 255 i.e. max pixelel value defined by graphics framework.
    assert that the caller will clamp it to 255 ???
    '''
    return result

  
  
  def updateFoodAt(self, automata, foodAt, consumed):  # foodAt is not used.
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
    assert consumed <= 255 
    
    yetToConsume = consumed
    
    for pixelelID in self.patch:
      foodAt = self.food.pixmap.getPixelel(pixelelID)
      if foodAt <= 0:
        continue
      # assert 0 < foodAt <= 255
      # Don't eat more from this pixel than ToConsume
      clamped = min(foodAt, yetToConsume)
      remainingFood = foodAt - clamped
      self.food.pixmap.setPixelel(pixelelID, remainingFood)
      yetToConsume -= clamped
      if yetToConsume <= 0:
        break
      
  """
  def clampValue(self, amount, clampValue):
    # Standard Python idiom for clamping in range [0, clampValue]
    return max(0, min(amount, clampValue))
  """
  
  