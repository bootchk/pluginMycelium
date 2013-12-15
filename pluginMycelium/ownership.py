'''

'''
class Ownership(object):
  '''
  PixMapMask that knows the channel that owns a Pixel
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
  
  
ownership = Ownership()
# Must still create()
