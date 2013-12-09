'''
'''

class AutomataFactory(object):
  '''
  Knows:
  - what subclass of Automata, according to user's configuration.
  - how to specialize instances with parameters, also according to user's configuration.
  
  A class IS-A factory (producer of instances).
  This adds another layer of factory: 
  a tool is a producer of instances,
  a factory contains a tool that may be swapped out for another tool, 
  and the tool may be configured.
  For now, this factory has no 'retool' method.
  '''
  
  
  def __init__(self, automataClass, bpp=1):
    self.automataClass = automataClass  # tooling
    self.bpp = bpp  # count of bytes per pixel (aka channels, aka resourceTypes) i.e. image mode
    
    self. lastChannel = 0


  def produce(self, **kwargs):
    '''
    Instance of some Automata subclass.
    '''
    if not 'channel' in kwargs:
      print("No channel to produce")
      '''
      '''
      return self.automataClass(channel=self.chooseChannel(), **kwargs )
    else:
      print("Channel to produce")
      return self.automataClass(**kwargs)
  
  
  def chooseChannel(self):
    '''
    Choose a channel (food, aka resource).
    
    Cycle through the channels.
    If bpp is 1, this always return 0 (the GRAY channel.)
    '''
    self.lastChannel += 1
    if self.lastChannel > self.bpp - 1:
      self.lastChannel = 0
    return self.lastChannel
     