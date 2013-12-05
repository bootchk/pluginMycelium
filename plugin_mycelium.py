#!/usr/bin/env python

'''
For dev in Eclipse: in proj properties>PyDev PYTHONPATH>External libraries, add: /usr/lib/Gimp/2.0/Python
'''


from gimpfu import *


def pluginMain(image, drawable, foo):
  ''' 
  Glue to code in a Python package in same directory as this. 
  (Keep plugin code separate from this wrapper code.
  '''
  from pluginMycelium.myceliumGimpPlugin import myceliumGimpPlugin
  
  myceliumGimpPlugin(image, drawable, foo)
  
  

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
                (PF_INT, "x_blur", "X blur", 9),
        ],
        [],
        pluginMain)

# Testing main
##def main():
##  myceliumGimpPlugin(1, 2, 3)
  
main()  # Call Gimp plugin main