'''
Parameters (aka configuration)
'''

'''
Mode parameters
'''
renderToGray = True


'''
Field parameters.
'''
startPattern = 0
maxPopulation = 0
terminationPercent = 0


'''
Automata parameters

30, 15, 25 dies quickly

As ratio, .3, .295, .15, are the original values.
Which as ratio times 255 is 76, 75, 38, 

As ratio .1, .05, .095 is finer grained.
Which as ratio times 255 is 26, 24, 13
'''
squirminess = 0
greedy = False
exhaustion = 0

mealCalories = 0  # how much an automata may eat per period
burnCalories = 0  # how much an automata metabolizes (from meal and reserves) each period
reservesToDivide = 0  # how much reserves are required to divide

'''
OLD names for these parameters

GUT_SIZE = 26  # 76
HEALTH_DAILY_METABOLISM = 24  # 75
HEALTH_TO_PROCREATE = 13  # 38
'''
