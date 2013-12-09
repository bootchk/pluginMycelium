'''
Main of Gimp plugin
'''

from gimpfu import *

from pixmap.pixmap import Pixmap

from simulator import AutomataSimulator
from automataFactory import AutomataFactory
from automata import Automata
from frame import Frame
from food import Food
from artifacts import Artifacts
from field import Field
import config


def myceliumGimpPlugin(image, drawable, startPattern, maxPopulation, squirminess, terminationPercent, greedy,
                       exhaustion, mealCalories, burnCalories, reservesToDivide):
  
  config.startPattern = startPattern
  config.maxPopulation = maxPopulation
  config.squirminess = squirminess
  config.terminationPercent = terminationPercent
  config.greedy = greedy
  config.exhaustion = exhaustion
  config.mealCalories = int(mealCalories)
  config.burnCalories = int(burnCalories)
  config.reservesToDivide = int(reservesToDivide)
  
  
  
  # From image create a gray pixmap (one byte of gray value per pixel) to be food
  grayPixmap = createGrayPixmapFromInImage(image)
  food = Food(grayPixmap) # wrap pixmap, consider it food
  
  # output images out
  outputPixmap = createOutImagePixmap(drawable)
  artifacts = Artifacts(outputPixmap) # wrap pixmap, consider it artifact
  
  frame=Frame( drawable.width, drawable.height )
  
  field=Field(automataFactory=AutomataFactory(Automata), food=food, artifacts=artifacts, frame=frame)
  field.populate()
  
  simulator = AutomataSimulator(frame=frame, field=field)
  simulator.simulate()
  simulator.flush()
  
  print("plugin done")
  
  '''
  No clean up: we only created one image that user will receive.  
  Output Pixmap was flushed.
  Both in and out Pixmap get garbage collected.
  '''
  


def createGrayPixmapFromInImage(image):
  grayscaleImage = copyImageToGrayscale(image)
  activeLayer = pdb.gimp_image_get_active_drawable(grayscaleImage)
  
  # Remove alpha channel if it has one (we don't use it, clogs pixmap, user may restore it.)
  pdb.gimp_layer_flatten(activeLayer)
  
  # !!! Invert it: convert black as small value to large value (of food.)
  # I.E. automatas consume black, and poop black
  pdb.gimp_invert(activeLayer)
  
  return Pixmap(activeLayer)


def createOutImagePixmap(drawable):
  ''' Create grey output image. '''
  width = drawable.width
  height = drawable.height
  
  outImage = gimp.Image(width, height, GRAY)  # <<< GRAY
  outImage.disable_undo()
  layer = gimp.Layer(outImage, "X Dots", width, height, GRAY_IMAGE, 100, NORMAL_MODE) # <<< GRAY
  outImage.add_layer(layer, 0)
  pdb.gimp_edit_fill(layer, BACKGROUND_FILL)
  
  displayID = pdb.gimp_display_new(outImage)  # Make it visible on screen
  
  outPixmap = Pixmap(layer) # create pixmap from Drawable, not Image
  return outPixmap
  
  
def copyImageToGrayscale(image):
  '''
  Copy of image converted to GRAY (might still  have ALPHA.)
  '''
  imageCopy = pdb.gimp_image_duplicate(image)
  
  # Convert RGB or INDEXED to GRAY
  if  imageCopy.base_type != GRAY:
    pdb.gimp_image_convert_grayscale(imageCopy)  
  return imageCopy
  
  
  