#!/usr/bin/env python

'''
For dev in Eclipse: in proj properties>PyDev PYTHONPATH>External libraries, add: /usr/lib/Gimp/2.0/Python
'''


from gimpfu import *


def pluginMain(image, drawable, startPattern, maxPopulation, terminationPercent, renderToGray, 
               squirminess, greedy, exhaustion, 
               mealCalories, burnCalories, reservesToDivide ):
  ''' 
  Glue to code in a Python package in same directory as this. 
  (Keep plugin code separate from this wrapper code.
  '''
  from pluginMycelium.myceliumGimpPlugin import myceliumGimpPlugin
  
  myceliumGimpPlugin(image, drawable, startPattern, maxPopulation, squirminess, terminationPercent, greedy,
                     exhaustion, mealCalories, burnCalories, reservesToDivide, renderToGray)
  

register(
        "python_fu_mycelium",
        "Make new image rendered by moving automata, feeding on the original.",
        "Make new image rendered by moving automata, feeding on the original.",
        "Lloyd Konneker",
        "Lloyd Konneker",
        "2013",
        "<Image>/Filters/Map/Mycelium...",
        "RGB*, GRAY*, INDEXED*",
        [
          (PF_OPTION, "startPattern", "Starting field:", 1, ["Centered", "Uniform"]), 
          (PF_SPINNER, "maxPopulation", "Max population:", 100, (1, 10000, 10)),
          (PF_SLIDER, "terminationPercent", "Ending percent:", 60, (1, 100, 10)),
          (PF_TOGGLE, "renderToGray",   "Mode to gray:", 1),
          (PF_OPTION, "squirminess","Myce squirm:", 0, ["Relaxed","Curly","Kinky"]),
          (PF_TOGGLE, "greedy",   "Myce greedy:", 0),
          (PF_OPTION, "exhaustion","Myce exhausted:", 1, ["Die","Migrate"]),
          (PF_SLIDER, "mealCalories", "Myce max daily intake:", 26, (1, 255, 10)),
          (PF_SLIDER, "burnCalories", "Myce daily burn:", 24, (1, 255, 10)),
          (PF_SLIDER, "reservesToDivide", "Myce divide on reserves of:", 13, (1, 255, 10)),
        ],
        [],
        pluginMain)

#(PF_RADIO, "startPattern", "Starting field:", 1, (("Centered", 0), ("Uniform", 1))), 
#(PF_RADIO, "exhaustion", "Exhaustion:", 1, (("Perish", 0), ("Migrate", 1), )),
#(PF_RADIO, "squirminess", "Squirminess:", 0, (("Relaxed", 0), ("Curly", 1), ("Kinky", 2))),


# Testing main
##def main():
##  myceliumGimpPlugin(1, 2, 3)
  
main()  # Call Gimp plugin main