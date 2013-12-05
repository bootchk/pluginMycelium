'''
'''
from config import MAX_POPULATION_COUNT as MAX_POPULATION_COUNT



class Field(object):
  '''
  A container and environ for automata.
  Resources: food and artifacts
  '''
  
  
  def __init__(self, food, artifacts):
    self.automata = []
    
    # Public
    self.food = food
    self.artifacts = artifacts
  
  
  def append(self, automata):
    self.automata.append(automata)
    print("append Automata ", len(self.automata) )
    
    
  def automataGenerator(self):
    ''' 
    Generate (in Python sense, not in family generation sense)
    
    !!! Since we are concurrently mutating (adding to) list, generate from copy.
    In Python, undefined behaviour to iterate over a mutating list.
    '''
    automataCopy = self.automata[:]
    for automata in automataCopy:
      yield automata
  
  def isCrowded(self):
    return len(self.automata) < MAX_POPULATION_COUNT
  
  
  