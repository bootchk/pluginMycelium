'''
'''

import config


class Compositor(object):
  '''
  Mixin behaviour for Artifacts.
  
  Determines compose method for depositing pixelel values.
  
  Compose from a meal.
  
  Meal might have consumed many pixelels:
  - neighbor pixel's pixelels
  - many pixelels of one pixel
  
  Meal might have more total value than can deposit in one pixelel (255.)
  
  Compose might change many pixelels (e.g. all pixelels of pixel)
  
  Compose might be shifting values from one pixelel to another.
  '''
  
  
  def dispatchComposeMethod(self):
    '''
    Method of composing (of combining pixelel values.  Of combining previous value with delta value.)
    
    Dispatched on setting.
    '''
    if config.compose == 0:
      return self.addingCompose
    elif config.compose == 1:
      return self.funnelingCompose
    elif config.compose == 2:
      return self.maximizeCompose
    elif config.compose == 3:
      return self.owningCompose
    elif config.compose == 4:
      return self.pixelAddingCompose
    else:
      return self.pixelOwningCompose
    
    
    
  '''
  Gradual compose, slowly build in value as automatas metabolize.
  '''

  # TODO this should not be max, but essential
  def addingCompose(self, automata, meal):
    '''
    Increment a single pixelel (channel) by max channel from meal.
    
    If meal ate from many pixelels, this may reduce brightness.
    '''
    pixelelID = automata.pixelelID()
    currentArtifact = self.pixmap.getPixelel(pixelelID)
    newArtifact = currentArtifact + meal.maxAmount()
    self.pixmap.setPixelel(pixelelID, newArtifact)
    
  
  def funnelingCompose(self, automata, meal):
    '''
    Increment a single pixelel (channel) by sum channels from meal.
    
    If meal ate from many pixelels, this reduces resolution
    and might reduce brightness.
    '''
    pixelelID = automata.pixelelID()
    currentArtifact = self.pixmap.getPixelel(pixelelID)
    newArtifact = currentArtifact + meal.size() # totalCalories
    newArtifact = min(newArtifact, 255)
    self.pixmap.setPixelel(pixelelID, newArtifact)
    
    
  def pixelAddingCompose(self, automata, meal):
    '''
    Increment all pixelels of artifacts by corresponding portions from meal.
    
    Automata are specialized to move on a channel.
    But here, they consume and deposit other channels of pixel of automata.
    
    For grayscale and singlePixelMouth, this is equivalent to addingCompose (since there are no other channels of pixel.)
    
    Note we already ate food, and this should not concern itself with food.
    '''
    for portion in meal.portions:
      channel = portion.pixelelID
      currentArtifact = self.pixmap.getPixelel(channel)
      newArtifact = currentArtifact + portion.amount
      # If meal is shifting values from one pixelel to another, must clamp
      newArtifact = min(newArtifact, 255)
      self.pixmap.setPixelel(channel, newArtifact)

  
  '''
  Abrupt compose, first to visit sets ultimate value as automatas metabolize.
  Further visits still eat and may change environment,
  so further visits have no effect on the pixelel, but are not redundant.
  '''
  
  # TODO is this called even if it did not eat in its channel??
  def maximizeCompose(self, automata, meal):
    '''
    Compose boolean: black 0 or white 255.
    
    Second visits are redundant: set it to same value again.
    
    meal not used.  Assert not meal.isEmpty()? But this might be a way to implement slime.
    '''
    self.pixmap.setPixelel(automata.pixelelID(), 255)
    
    ## ORIGINAL FOR HARDCODED CHANNEL
    ## self.pixmap[pixelelID] = array('B', (0, ))
  
  
  """
  # NOT Used
  def replaceCompose(self, automata, amount):
    '''
    Value given by the last (in time) to visit.
    '''
    pixelelID = automata.pixelelID()
    # monotonic, not remainder
    newValue = 255-amount
    if newValue < self.pixmap.getPixelel(pixelelID):
      # Clear other pixelels
      self.pixmap[pixelelID.coord]=array('B', (0,0,0))
    
      self.pixmap.setPixelel(pixelelID, newValue)
  
      
  # NOT USED
  def decrementCompose(self, automata, meal):
    '''
    Subtract: Gimp is a brightness 'value' where larger is whiter, subtract amount towards black.
    '''
    pixelelID = automata.pixelelID()
    currentArtifact = self.pixmap.getPixelel(pixelelID)
    newArtifact = currentArtifact - meal
    if newArtifact < 0:
      newArtifact = 0 # clamp
    self.pixmap.setPixelel(pixelelID, newArtifact)
    
    ## ORIGINAL FOR HARDCODED CHANNEL
    ## self.pixmap[position] = array('B', (newArtifact, ))
  
    
  # NOT Used
  def firstCompose(self, automata, amount):
    '''
    Value given by first to visit this pixel,
    and only deposit the first meal (on my first visit.)
    '''
    # assert pixelels were all initialized to 255 (white)
    pixelelID = automata.pixelelID()
    pixel = self.pixmap[pixelelID.coord]
    
    first = True
    for pixelel in pixel:
      if pixelel < 255:
        first = False
        break
    
    if first:
      self.pixmap.setPixelel(pixelelID, 255-amount)
  """   
  
  def owningCompose(self, automata, amount):
    '''
    Only deposit if an automata of my channel class was first to visit this pixel,
    but increment pixelel value with meals from second visits.
    I.E. once a pixel is first visited by an automata, all automata having the same channel can deposit.
    '''
    owned, visitedPixelelID = self.isOwned(automata.pixelelID())
    
    if not owned:
      '''
      No channel class owns it (I am first to visit.)
      Composing from it establishes ownership.
      '''
      self.addingCompose(automata, amount)
    else:
      '''
      Some channel class of automata owns it.  If that channel matches my channel, compose.
      '''
      if visitedPixelelID == automata.pixelelIndex:
        self.addingCompose(automata, amount)
  
  
  def pixelOwningCompose(self, automata, amount):
    '''
    Only deposit if an automata of my channel class was first to visit this pixel.
    '''
    owned, visitedPixelelID = self.isOwned(automata.pixelelID())
    
    if not owned:
      '''
      No channel class owns it (I am first to visit.)
      Composing from it establishes ownership.
      '''
      self.pixelAddingCompose(automata, amount)
    else:
      '''
      Some channel class of automata owns it.  If that channel matches my channel, compose.
      '''
      if visitedPixelelID == automata.pixelelIndex:
        self.pixelAddingCompose(automata, amount)
        
  
  '''
  TODO this is not correct for certain mouths.
  '''
  def isOwned(self, pixelelID):
    ''' 
    Whether some channel (pixelelIndex) class of automata owns, and which channel class owns it.
    Is pixel owned by class of automata of certain channel? 
    '''
    
    # assert pixelels were all initialized to 0 (black)
    # WAS 255 (white)
    pixel = self.pixmap[pixelelID.coord]
    
    owned = False
    pixelelIndex = 0
    for pixelel in pixel:
      if pixelel > 0:  # WAS < 255:
        owned = True
        break
      pixelelIndex += 1
      
    # Logically, 'x implies y' is equivalent to '(not x) or y'
    # Thus 'owned implies pixelelIndex<pixmap.bpp' is equivalent to as follows:
    assert (not owned) or pixelelIndex < self.pixmap.bpp
    return owned, pixelelIndex
  
  
  
    