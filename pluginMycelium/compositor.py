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
    
  
  def incrementCompose(self, pixelelID, amount):
    '''
    Composes not binary, slowly build in value as automatas metabolize.
    '''
    # Subtract: Gimp is a brightness 'value' where larger is whiter, subtract amount towards black.
    currentArtifact = self.pixmap.getPixelel(pixelelID)
    newArtifact = currentArtifact - amount
    if newArtifact < 0:
      newArtifact = 0 # clamp
    self.pixmap.setPixelel(pixelelID, newArtifact)
    
    ## ORIGINAL FOR HARDCODED CHANNEL
    ## self.pixmap[position] = array('B', (newArtifact, ))
    
  
  def maximizeCompose(self, pixelelID, amount):
    '''
    Compose boolean: black 0 or white 255.
    
    Second visits are redundant: set it to same value again.
    
    amount not used
    '''
    self.pixmap.setPixelel(pixelelID, 0)
    
    ## ORIGINAL FOR HARDCODED CHANNEL
    ## self.pixmap[pixelelID] = array('B', (0, ))
  
  
  def replaceCompose(self, pixelelID, amount):
    # monotonic, not remainder
    newValue = 255-amount
    if newValue < self.pixmap.getPixelel(pixelelID):
      # Clear other pixelels
      self.pixmap[pixelelID.coord]=array('B', (0,0,0))
    
      self.pixmap.setPixelel(pixelelID, newValue)
    
    
  def firstCompose(self, pixelelID, amount):
    '''
    Only deposit if I am first to visit this pixel,
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
    Only deposit if I am first to visit this pixel,
    but increment pixelel value with meals from second visits.
    I.E. once I visit a pixel, I own it.
    '''
    # assert pixelels were all initialized to 255 (white)
    pixel = self.pixmap[pixelelID.coord]
    
    first = True
    pixelelIndex = 0
    for pixelel in pixel:
      if pixelel < 255:
        first = False
        break
      pixelelIndex += 1
    
    # x=>y is equivalent to (not x) or y
    
    # first => pixelelIndex==pixmap.bpp
    assert (not first) or pixelelIndex == self.pixmap.bpp
    
    # If first, or not the first but previous visitor visited same pixelel (channel)
    if first or (pixelelIndex < self.pixmap.bpp and pixelelIndex == pixelelID.pixelelIndex):
      self.incrementCompose(pixelelID, amount)
    