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
    return self.automataClass(**kwargs)