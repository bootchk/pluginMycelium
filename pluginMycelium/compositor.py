'''
'''
from array import array

import config


class Compositor(object):
  '''
  Mixin behaviour for Artifacts.
  
  Determines compose method for depositing pixelel values.
  '''
  
  
  def dispatchComposeMethod(self):
    '''
    Method of composing (of combining pixelel values.  Of combining previous value with delta value.)
    
    Dispatched on setting.
    '''
    if config.compose == 0:
      return self.incrementCompose
    elif config.compose == 1:
      return self.ownCompose
    else:
      return self.maximizeCompose
    
  '''
  Gradual compose, slowly build in value as automatas metabolize.
  '''
  # NOT USED
  def decrementCompose(self, pixelelID, amount):
    '''
    Subtract: Gimp is a brightness 'value' where larger is whiter, subtract amount towards black.
    '''
    currentArtifact = self.pixmap.getPixelel(pixelelID)
    newArtifact = currentArtifact - amount
    if newArtifact < 0:
      newArtifact = 0 # clamp
    self.pixmap.setPixelel(pixelelID, newArtifact)
    
    ## ORIGINAL FOR HARDCODED CHANNEL
    ## self.pixmap[position] = array('B', (newArtifact, ))
    
    
  def incrementCompose(self, pixelelID, amount):
    '''
    Increment a single channel by amount.
    '''
    currentArtifact = self.pixmap.getPixelel(pixelelID)
    newArtifact = currentArtifact + amount
    newArtifact = min(newArtifact, 255)
    self.pixmap.setPixelel(pixelelID, newArtifact)
    
    
  def incrementPixelCompose(self, pixelelID, amount):
    '''
    Increment all channels by amount.
    '''
    currentArtifact = self.pixmap.getPixelel(pixelelID)
    newArtifact = currentArtifact + amount
    newArtifact = min(newArtifact, 255)
    self.pixmap.setPixelel(pixelelID, newArtifact)
  
  
  def maximizeCompose(self, pixelelID, amount):
    '''
    Compose boolean: black 0 or white 255.
    
    Second visits are redundant: set it to same value again.
    
    amount not used
    '''
    self.pixmap.setPixelel(pixelelID, 255)
    
    ## ORIGINAL FOR HARDCODED CHANNEL
    ## self.pixmap[pixelelID] = array('B', (0, ))
  
  
  # NOT Used
  def replaceCompose(self, pixelelID, amount):
    '''
    Value given by the last (in time) to visit.
    '''
    # monotonic, not remainder
    newValue = 255-amount
    if newValue < self.pixmap.getPixelel(pixelelID):
      # Clear other pixelels
      self.pixmap[pixelelID.coord]=array('B', (0,0,0))
    
      self.pixmap.setPixelel(pixelelID, newValue)
    
  # NOT Used
  def firstCompose(self, pixelelID, amount):
    '''
    Value given by first to visit this pixel,
    and only deposit the first meal (on my first visit.)
    '''
    # assert pixelels were all initialized to 255 (white)
    pixel = self.pixmap[pixelelID.coord]
    
    first = True
    for pixelel in pixel:
      if pixelel < 255:
        first = False
        break
    
    if first:
      self.pixmap.setPixelel(pixelelID, 255-amount)
      
  
  def ownCompose(self, pixelelID, amount):
    '''
    Only deposit if an automata of my channel class was first to visit this pixel,
    but increment pixelel value with meals from second visits.
    I.E. once a pixel is first visited by an automata, all automata having the same channel can deposit.
    '''
    owned, visitedPixelelID = self.isOwned(pixelelID)
    
    if not owned:
      '''
      No channel class owns it (I am first to visit.)
      Composing from it establishes ownership.
      '''
      self.incrementCompose(pixelelID, amount)
    else:
      '''
      Some channel class of automata owns it.  If that channel matches my channel, compose.
      '''
      if visitedPixelelID == pixelelID.pixelelIndex:
        self.incrementCompose(pixelelID, amount)
    
  
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
  
  
  
    