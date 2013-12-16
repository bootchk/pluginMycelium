'''
'''

class Stagnator(object):
  '''
  Determines lack of change to a variable over time.
  
  Stagnant: greater than 10 consecutive periods with small change to value
  '''
  
  def __init__(self):
    self.previousValue = None
    self.countStagnantPeriods = 0
  
  
  
  def isStagnant(self, newValue):
    ''' 
    is delta value approaching limit of zero?
    Where delta value is difference of newValue from newValue on prior call.
    '''
    if self.previousValue is None:
      # First time ever called
      result = False
    else:
      delta = newValue - self.previousValue
      if delta < 20:
        self.countStagnantPeriods += 1
        if self.countStagnantPeriods > 10:
          print "Stagnated"
          result = True
        else:
          result = False
      else:
        self.countStagnantPeriods = 0 # reset count
        result = False
    
    #print "isStagnant", self.previousValue, newValue
    self.previousValue = newValue  # Always roll
    assert result == True or result == False
    return result