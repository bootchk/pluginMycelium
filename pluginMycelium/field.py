'''
'''
import random

from automata import Automata
from pixmap.coord import Coord

import config



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
    return len(self.automata) >= config.maxPopulation
  

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
    if config.startPattern == 0:
      self.populateCenter()
    else:
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
    Spread populus uniformly randomly over the field.
    '''
    # ??? if user does not touch population, is a float?  So cast it to int.
    assert config.maxPopulation > 0
    for i in range(0, int(config.maxPopulation)):
      x = random.randint(0, self.frame.width)
      y = random.randint(0, self.frame.height)
      coord = Coord(x, y)
      automata = Automata(position=coord, field=self)
      self.append(automata)
      
  