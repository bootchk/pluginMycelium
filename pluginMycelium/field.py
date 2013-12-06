'''
'''
import random

from automata import Automata
from pixmap.coord import Coord

from config import MAX_POPULATION_COUNT as MAX_POPULATION_COUNT



class Field(object):
  '''
  A container and environ for automata.
  Resources: food and artifacts
  '''
  
  
  def __init__(self, food, artifacts, frame):
    self.automata = []
    
    # Public
    self.food = food
    self.artifacts = artifacts
    self.frame = frame
  
  
  def append(self, automata):
    self.automata.append(automata)
    print("append Automata ", len(self.automata) )
    pass
    
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
  
  
  def populate(self):
    '''
    Dispatch populate on setting.
    '''
    ##self.populateCenter()
    self.populateUniformly()
  
  
  def populateCenter(self):
    '''
    Populate one automata in center.
    If the center has no food the simulation will stop immediately?
    '''
    automata = Automata(position=self.frame.center(), field=self)
    self.append(automata)


  def populateUniformly(self):
    '''
    Spread a population of 100 uniformly randomly over the field.
    '''
    for i in range(0, 100):
      x = random.randint(0, self.frame.width)
      y = random.randint(0, self.frame.height)
      coord = Coord(x, y)
      automata = Automata(position=coord, field=self)
      self.append(automata)
      
  