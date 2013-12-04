'''

'''
import random

from copy import copy
from direction import Direction
from pixmap.coord import Coord


from config import HEALTH_TO_PROCREATE as HEALTH_TO_PROCREATE
from config import HEALTH_DAILY_METABOLISM as HEALTH_DAILY_METABOLISM


  
class Cell(object):
  ''' Cellular automata '''
  
  
  def __init__(self, position, field, direction=None, health=None):
    assert position is not None
    assert field is not None
    self.position = copy(position) # !!! copy
    self.field = field  # a cell knows its field
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
    '''
    self.changeHealth()
    self.move()
    self.changeDirection()
    self.tryDivide()
    self.tryMigrate()
    self.tryPoop()
    
    
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
    '''
    self.healthState += self.field.food.eat(self.position) - HEALTH_DAILY_METABOLISM
    if self.healthState <= 0:
      self.setStarved()
    
    
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
    ''' If I am healthy enough, and the field is not too crowded, divide. '''
    if self.healthState > HEALTH_TO_PROCREATE and not self.field.isCrowded():
      self.divide()
      
      
  def divide(self):
    ''' 
    Spawn a new cell.
    
    '''
    # Divide self's health evenly
    self.healthState /= 2 # integer divide
    
    # child and parent directions diverge, slightly left and right
    left, right = self.direction.fork()
    self.direction = left
    
    # Parent and child in same position.
    newCell = Cell(position=self.position, field=self.field, health=self.healthState, direction=right)
    
    ## ALTERNATIVE  child move in opposite direction
    ## newCell.direction.setOpposite(self.direction)
    
    self.field.appendCell(newCell)
  
    
  def tryMigrate(self):
    if self.isStarved():
      self.migrate()
      
      
  def tryPoop(self):
    ''' 
    Artifact of metabolism i.e. eating.
    
    Self need not be starved.  But may not be eating.
    Self may be healthy but wandered off field.
    
    Note that self moved first, so current position may have enough food to eat,
    but current health is a result from previous positio.
    '''
    # if self.isEating():
    if not self.isStarved():
      print("Pooped at", self.position)
      self.field.artifacts.depositAt(self.position)
      
    