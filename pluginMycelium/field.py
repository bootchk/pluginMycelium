'''
'''
from config import MAX_POPULATION_COUNT as MAX_POPULATION_COUNT



class Field(object):
  '''
  A container and environ for cells.
  Resources: food and artifacts
  '''
  
  
  def __init__(self, food, artifacts):
    self.cells = []
    
    # Public
    self.food = food
    self.artifacts = artifacts
  
  
  def appendCell(self, cell):
    self.cells.append(cell)
    print("append Cell ", len(self.cells) )
    
    
  def cellGenerator(self):
    ''' 
    Generate (in Python sense, not in family generation sense)
    
    !!! Since we are concurrently mutating (adding to) list, generate from copy.
    In Python, undefined behaviour to iterate over a mutating list.
    '''
    cellsCopy = self.cells[:]
    for cell in cellsCopy:
      yield cell
  
  def isCrowded(self):
    return len(self.cells) < MAX_POPULATION_COUNT