'''

'''
import random

from copy import copy
from direction import Direction
from pixmap.coord import Coord


import config
#from config import HEALTH_TO_PROCREATE as HEALTH_TO_PROCREATE
#from config import HEALTH_DAILY_METABOLISM as HEALTH_DAILY_METABOLISM


  
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
  
  
  def __init__(self, position, field, direction=None, reserves=None):
    assert position is not None
    assert field is not None
    self.position = copy(position) # !!! copy
    self.field = field  # a automata knows its field
    if reserves is None:
      self._reserves = 0
    else:
      self._reserves = reserves
    if direction is None:
      self.direction = Direction()
    else:
      self.direction = direction
    
    # Set behaviour by binding to one of two methods
    if config.greedy:
      self.changeDirectionMethod = self._greedyChangeDirection
    else:
      self.changeDirectionMethod = self._nonGreedyChangeDirection
    
    
  def live(self):
    '''
    Behaviour: do every life cycle.
    
    !!! It is not invariant that current position is on the field.
    '''
    # eat and poop at current position, if it is on the field !!!
    meal = self.metabolize() 
    self.tryPoop(meal)
    
    # Change direction just before move, otherwise other automata may swoop in and eat what I am greedily changing direction toward
    self.changeDirection()
    self.move()
    
    self.tryDivide()
    self.tryExhaustion(meal)
    
    
    
  def isEating(self):
    return self.field.food.isAvailableAt(self.position)
  
  def isStarved(self):
    return self._reserves == 0
  
  def setStarved(self):
    ##print("Starved", self.position)
    self._reserves = 0
  

  def metabolize(self):
    '''
    Try to eat.  Return size of meal eaten.
    Adjust reserves.
    '''
    meal = self.field.food.eat(self.position)
    # A meal larger than metabolic rate increases reserves.
    self._reserves +=  meal - config.burnCalories
    if self._reserves <= 0:
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
    
    TODO this should be a fraction of the image size
    '''
    randomCoord = Coord(random.randint(-15, 15), random.randint(-15, 15))
    self.position = self.position + randomCoord
    ##print("migrate to", self.position)
    
  
  def changeDirection(self):
    '''
    Random direction change from set [ diagonally left of current direction, diagonally right of current direction]
    (Not hard left, or reverse.)
    '''
    # Call the method bound at init time
    # TODO subclasses and factories
    self.changeDirectionMethod()
  
  
  def _nonGreedyChangeDirection(self):
    '''
    Random direction change from set [ diagonally left of current direction, diagonally right of current direction]
    (Not hard left, or reverse.)
    '''
    self.direction.tweak()
    
    
  def _greedyChangeDirection(self):
    '''
    Greedy: choose direction toward more food.
    '''
    left, right = self.direction.fork()
    leftNeighbor = self.position + left.unitCoordFor()
    rightNeighbor = self.position + right.unitCoordFor()
    # TODO this biases toward right when neighbors equal
    if self.field.food.at(leftNeighbor) > self.field.food.at(rightNeighbor) :
      self.direction = left
    else:
      self.direction = right
  
  
  def tryDivide(self):
    ''' If self has enough reserves, and the field is not overpopulated, divide. '''
    if self._reserves > config.reservesToDivide and not self.field.isOverPopulated():
      self.divide()
      
      
  def divide(self):
    ''' 
    Spawn a new automata.
    '''
    
    # Divide self's reserves evenly
    self._reserves /= 2 # integer divide
    
    # child and parent directions diverge, slightly left and right
    left, right = self.direction.fork()
    self.direction = left
    
    # Parent and child in same position.
    newAutomata = Automata(position=self.position, field=self.field, reserves=self._reserves, direction=right)
    
    ## ALTERNATIVE  child move in opposite direction
    ## newAutomata.direction.setOpposite(self.direction)
    
    self.field.append(newAutomata)
  
    
  def tryExhaustion(self, meal):
    '''
    Test whether exhausted: starved and did not eat.
    
    Alternative: migrate if starved regardless whether we ate.
    '''
    if self.isStarved() and meal <= 0:
      if config.exhaustion == 0:
        '''
        Perish: remove myself from population.
        Self will be garbage collected.
        Some other automate may repopulate (by dividing.)
        '''
        self.field.kill(self)
      else:
        self.migrate()
      
      
  def tryPoop(self, meal):
    ''' 
    Artifact of metabolism i.e. eating.
    
    Self need not be exhausted (might have reserves).  But might not have just eaten (meal might be 0.)
    Self may have reserves but wandered off field.
    
    Whether current position has food, is on the field, etc. depends on the order in which sub-behaviours are called.
    
    TODO meal is what I consumed this period, not what is in my gut from last period.
    '''
    # if self.isEating():
    
    '''
    Note we may have just eaten, but could still be starved, if we did not eat enough to equal our daily metabolism.
    '''
    ##self._poopMealIfNotStarved(meal)
    self._poopMealIfAte(meal)
    
    
  # Alternative 1
  def _poopMealIfNotStarved(self, meal):
    '''
    Poop meal if not starved.
    Not true to life as we know it:
    - should poop yesterday's meal.
    - should poop if gut is not empty, regardless of starving state
    '''
    if not self.isStarved():
      # !!! Cannot assert: not isClipped(self.position)
      self.field.artifacts.depositAt(self.position, amount=meal)
      
      
  # Alternative 2
  def _poopMealIfAte(self, meal):
    # Assert this will not alter artifacts if meal is zero
    self.field.artifacts.depositAt(self.position, amount=meal)
  
  
    