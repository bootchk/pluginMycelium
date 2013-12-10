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
                       exhaustion, mealCalories, burnCalories, reservesToDivide,
                       renderToGray, compose):
  
  config.startPattern = startPattern
  config.maxPopulation = maxPopulation
  config.squirminess = squirminess
  config.terminationPercent = terminationPercent
  config.greedy = greedy
  config.exhaustion = exhaustion
  config.mealCalories = int(mealCalories)
  config.burnCalories = int(burnCalories)
  config.reservesToDivide = int(reservesToDivide)
  config.renderToGray = renderToGray
  config.compose = compose
  
  
  # From image create an input pixmap to be food
  inputPixmap = createInputPixmap(image)
  food = Food(inputPixmap) # wrap pixmap, consider it food
  
  # output images out
  outputPixmap = createOutImagePixmap(image, drawable)
  artifacts = Artifacts(outputPixmap) # wrap pixmap, consider it artifact
  
  frame=Frame( drawable.width, drawable.height )
  
  field=Field(automataFactory=AutomataFactory(Automata, bpp=outputPixmap.bpp), food=food, artifacts=artifacts, frame=frame)
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
  
  
  
'''
Much of what follows is about image mode.
It is possible for the plugin to produce only grayscale.
(And that was the original design.)
And that is probably the most common use case.
And a user could use a grayscale plugin to render in colors by decompose, execute, recompose on color channels.
So this is largely for user convenience.

Except that the effect 'colored worms but only the top worm displays'
might not be easily doable by a user with only a grayscale plugin.
'''
  
def createInputPixmap(image):
  '''
  Create a pixmap according to settings.
  But we ignore any selection.
  '''
  if isPluginModeGray(image):
    result = createGrayPixmapFromInImage(image)
  else:
    result = createColorPixmapFromInImage(image)
  return result
    
    
def isPluginModeGray(image):
  '''
  Do user's settings and input image force mode of Mycelium plugin to 'color'
  '''
  if config.renderToGray:
    result = True
  else:
    if image.base_type == RGB:
      result = False
    else:
      # Despite user's choice of rendreturnerToGray==False, image is already GRAY or INDEXED and can only be rendered GRAY
      result = True
  return result
  

def createGrayPixmapFromInImage(image):
  grayscaleImage = copyImageToGrayscale(image)
  return flattenInvertAndToPixmap(grayscaleImage)
  
  
def createColorPixmapFromInImage(image):
  # We need a copy because user can continue to use Gimp?
  colorImageCopy = pdb.gimp_image_duplicate(image)
  return flattenInvertAndToPixmap(colorImageCopy)
  


def flattenInvertAndToPixmap(image):
  activeLayer = pdb.gimp_image_get_active_drawable(image)
  
  # Remove alpha channel if it has one (we don't use it, clogs pixmap, user may restore it.)
  pdb.gimp_layer_flatten(activeLayer)
  
  # !!! Invert it: convert black as small value to large value (of food.)
  # I.E. automatas consume black, and poop black
  pdb.gimp_invert(activeLayer)
  
  return Pixmap(activeLayer)


def createOutImagePixmap(image, drawable):
  if isPluginModeGray(image):
    result = createGrayOutImagePixmap(drawable)
  else:
    result = createColorOutImagePixmap(drawable)
  return result


def createGrayOutImagePixmap(drawable):
  width = drawable.width
  height = drawable.height
  
  outImage = gimp.Image(width, height, GRAY)  # <<< GRAY
  outImage.disable_undo()
  layer = gimp.Layer(outImage, "Mycelium", width, height, GRAY_IMAGE, 100, NORMAL_MODE) # <<< GRAY
  outImage.add_layer(layer, 0)
  return fillDisplayAndToPixmap(outImage, layer)


def createColorOutImagePixmap(drawable):
  width = drawable.width
  height = drawable.height
  
  outImage = gimp.Image(width, height, RGB)
  outImage.disable_undo()
  layer = gimp.Layer(outImage, "Mycelium", width, height, RGB_IMAGE, 100, NORMAL_MODE)
  outImage.add_layer(layer, 0)
  return fillDisplayAndToPixmap(outImage, layer)
  
  
def fillDisplayAndToPixmap(outImage, layer):
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
  
  
  