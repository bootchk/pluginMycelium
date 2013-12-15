'''

'''
class Ownership(object):
  '''
  PixMapMask that knows the channel that owns a Pixel
  
  Value of mask byte is 3 if unowned, else the index of owning channel in range [0,2]
  '''
  def create(self, pixmap):
    self.mask = pixmap.selectionMask().getInitializedCopy(value=3)
    
  def isOwned(self, pixelelID):
    ''' 
    Whether any channel (pixelelIndex) class of automata owns, and whether the given channel class owns it.
    Is pixel owned by class of automata of certain channel? 
    '''
    maskValue = self.mask[pixelelID.coord]
    isOwned =  maskValue != 3
    selfOwned = maskValue == pixelelID.pixelelIndex
    return isOwned, selfOwned
  
  def possess(self, pixelelID):
    ''' Possess by putting my pixelelIndex in the mask. '''
    self.mask[pixelelID.coord] = pixelelID.pixelelIndex
  

# Singleton
ownership = Ownership()
# Must still call create()
