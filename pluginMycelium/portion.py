'''
'''

class Portion(object):
  '''
  Part of a meal.
  A pixelel value that knows its location.
  '''
  
  def __init__(self, pixelelID, amount):
    self.pixelelID = pixelelID
    self.amount = amount