#!/usr/bin/env python

'''
For dev in Eclipse: in proj properties>PyDev PYTHONPATH>External libraries, add: /usr/lib/Gimp/2.0/Python
'''


from gimpfu import *


def pluginMain(image, drawable, startPattern, maxPopulation, squirminess, terminationPercent):
  ''' 
  Glue to code in a Python package in same directory as this. 
  (Keep plugin code separate from this wrapper code.
  '''
  from pluginMycelium.myceliumGimpPlugin import myceliumGimpPlugin
  
  myceliumGimpPlugin(image, drawable, startPattern, maxPopulation, squirminess, terminationPercent)
  
  

register(
        "python_fu_mycelium",
        "Render black and white using mycelium (worm automata.)",
        "Make the specified layer look like it is printed on cloth",
        "James Henstridge",
        "James Henstridge",
        "1997-1999",
        "<Image>/Filters/Artistic/Mycelium...",
        "RGB*, GRAY*",
        [
          (PF_RADIO, "startPattern", "Starting field:", 1, (("Centered", 0), ("Uniform", 1))), 
          (PF_SPINNER, "maxPopulation", "Max population:", 100, (1, 1000, 10)),
          (PF_RADIO, "squirminess", "Squirminess:", 0, (("Relaxed", 0), ("Curly", 1), ("Kinky", 2))),
          (PF_SLIDER, "terminationPercent", "Ending (percent):", 60, (1, 100, 10)),
        ],
        [],
        pluginMain)

# Testing main
##def main():
##  myceliumGimpPlugin(1, 2, 3)
  
main()  # Call Gimp plugin main