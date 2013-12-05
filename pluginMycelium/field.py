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
  
  
  '''
  Population limit implies little about density: all automata could be crowded together.
  '''
  def isOverPopulated(self):
    return len(self.automata) >= MAX_POPULATION_COUNT
  

  def isTerminal(self):
    '''
    Generic: is conditions to end simulation?
    
    Specific: is most of the food gone.  (Not explicitly depend on population.)
    
    Many other formulations are possible.
    The formulation: 'is every automata starved' didn't work well, ended simulation with much food remaining.
    '''
    return self.food.isMostlyGone()
  
  
  