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
  
  
  def __init__(self, automataClass):
    self.automataClass = automataClass  # tooling


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
    Choose a channel (food, aka resource)
     It defaults to 0, but here we choose it according to user's choice of output image.
     
    If output is color, choose one of the RGB channels.
    Else choose the GRAY channel
    '''
    return 0
     