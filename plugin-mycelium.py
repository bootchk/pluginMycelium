#!/usr/bin/env python

'''
For dev in Eclipse: in proj properties>PyDev PYTHONPATH>External libraries, add: /usr/lib/Gimp/2.0/Python
'''


from gimpfu import *


def pluginMain(image, drawable, startPattern, maxPopulation, terminationPercent, squirminess, greedy,
               exhaustion, mealCalories, burnCalories, reservesToDivide ):
  ''' 
  Glue to code in a Python package in same directory as this. 
  (Keep plugin code separate from this wrapper code.
  '''
  from pluginMycelium.myceliumGimpPlugin import myceliumGimpPlugin
  
  myceliumGimpPlugin(image, drawable, startPattern, maxPopulation, squirminess, terminationPercent, greedy,
                     exhaustion, mealCalories, burnCalories, reservesToDivide)
  

register(
        "python_fu_mycelium",
        "Render grayscale using worm automata.",
        "Make a new image",
        "Lloyd Konneker",
        "Lloyd Konneker",
        "2013",
        "<Image>/Filters/Render/Mycelium...",
        "RGB*, GRAY*, INDEXED*",
        [
          (PF_RADIO, "startPattern", "Starting field:", 1, (("Centered", 0), ("Uniform", 1))), 
          (PF_SPINNER, "maxPopulation", "Max population:", 100, (1, 1000, 10)),
          (PF_SLIDER, "terminationPercent", "Ending (percent):", 60, (1, 100, 10)),
          (PF_RADIO, "squirminess", "Squirminess:", 0, (("Relaxed", 0), ("Curly", 1), ("Kinky", 2))),
          (PF_TOGGLE, "greedy",   "Greedy:", 0),
          (PF_RADIO, "exhaustion", "Exhaustion:", 1, (("Perish", 0), ("Migrate", 1), )),
          (PF_SLIDER, "mealCalories", "Meal calories:", 26, (1, 255, 10)),
          (PF_SLIDER, "burnCalories", "Daily burn:", 24, (1, 255, 10)),
          (PF_SLIDER, "reservesToDivide", "Reserves to procreate:", 13, (1, 255, 10)),
          
        ],
        [],
        pluginMain)

# Testing main
##def main():
##  myceliumGimpPlugin(1, 2, 3)
  
main()  # Call Gimp plugin main