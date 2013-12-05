'''

'''
import random

from copy import copy
from direction import Direction
from pixmap.coord import Coord


from config import HEALTH_TO_PROCREATE as HEALTH_TO_PROCREATE
from config import HEALTH_DAILY_METABOLISM as HEALTH_DAILY_METABOLISM


  
class Automata(object):
  ''' 
  Worm automata: it moves.  
  Contrast with cellular automata, where each automata is usually stationary (on a cell of a grid.)
  A worm automata is like a single-celled, motile, biological organism.
  
  See 'Patterson worms':
  - move only one unit, in only 6 directions on a triangular grid
  - die if there is no food (no direction not already traversed.)
  - only one worm exists at a time
  
  This is different from a Patterson worm:
  - there can be many worms on the same field
  - they can divide
  - each worm can move in 8 directions on a rectangular grid.
  - worms can move off the field (wander), and then MIGHT wander back on to the field.
  - worms if starved can migrate (jump more than one step, in more than 8 directions), again even off the field
  - worms if starved don't die, they continue to move and migrate (they just don't poop.)
  '''
  
  
  def __init__(self, position, field, direction=None, health=None):
    assert position is not None
    assert field is not None
    self.position = copy(position) # !!! copy
    self.field = field  # a automata knows its field
    if health is None:
      self.healthState = 0
    else:
      self.healthState = health
    if direction is None:
      self.direction = Direction()
    else:
      self.direction = direction
    
    
  def live(self):
    '''
    Behaviour: do every life cycle.
    
    !!! It is not invariant that current position is on the field.
    '''
    # eat and poop at current position, if it is on the field !!!
    meal = self.changeHealth() 
    self.tryPoop(meal)
    
    self.move()
    self.changeDirection()
    self.tryDivide()
    self.tryMigrate()
    
    
    
  def isEating(self):
    return self.field.food.isAvailableAt(self.position)
  
  def isStarved(self):
    return self.healthState == 0
  
  def setStarved(self):
    print("Starved", self.position)
    self.healthState = 0
  
  
  def changeHealth(self):
    '''
    Eating increases health, and just living decreases health.
    Return size of meal eaten.
    '''
    meal = self.field.food.eat(self.position)
    self.healthState +=  meal - HEALTH_DAILY_METABOLISM
    if self.healthState <= 0:
      self.setStarved()
    return meal
    
    
  def move(self):
    '''  
    To adjacent pixel in self.direction. May move out of frame.
    '''
    self.position = self.position + self.direction.unitCoordFor()
  
  
  def migrate(self):
    '''
    To pixel farther away, in a random direction.
    '''
    
    randomCoord = Coord(random.randint(-15, 15), random.randint(-15, 15))
    self.position = self.position + randomCoord
    print("migrate to", self.position)
    
  
  def changeDirection(self):
    '''
    Direction changes from diagonally left of current direction to diagonally right of current direction.
    (Not hard left, or reverse.)
    '''
    self.direction.tweak()
  
  
  def tryDivide(self):
    ''' If I am healthy enough, and the field is not overpopulated, divide. '''
    if self.healthState > HEALTH_TO_PROCREATE and not self.field.isOverPopulated():
      self.divide()
      
      
  def divide(self):
    ''' 
    Spawn a new automata.
    
    '''
    # Divide self's health evenly
    self.healthState /= 2 # integer divide
    
    # child and parent directions diverge, slightly left and right
    left, right = self.direction.fork()
    self.direction = left
    
    # Parent and child in same position.
    newAutomata = Automata(position=self.position, field=self.field, health=self.healthState, direction=right)
    
    ## ALTERNATIVE  child move in opposite direction
    ## newAutomata.direction.setOpposite(self.direction)
    
    self.field.append(newAutomata)
  
    
  def tryMigrate(self):
    if self.isStarved():
      self.migrate()
      
      
  def tryPoop(self, meal):
    ''' 
    Artifact of metabolism i.e. eating.
    
    Self need not be starved.  But may not be eating.
    Self may be healthy but wandered off field.
    
    Whether current position has food, is on the field, etc. depends on the order in which sub-behaviours are called.
    '''
    # if self.isEating():
    
    '''
    Note we may have just eaten, but could still be starved, if we did not eat enough to equal our daily metabolism.
    Note this is ignoring meal, and we may be depositing more than the meal (yesterday's meal.)
    '''
    if not self.isStarved():
      # !!! Cannot assert: not isClipped(self.position)
      self.field.artifacts.depositAt(self.position)
      
    