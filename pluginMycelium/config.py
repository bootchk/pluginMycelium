'''
Parameters (aka configuration)
'''

'''
Automata parameters

30, 15, 25 dies quickly

As ratio, .3, .15, .295 the original?
Which as ratio to 255 is 76, 38, 75

.1, .05, .095
26, 13, 24
'''
# how much health a automata may eat (gain) per period
GUT_SIZE = 26  # 76

# how much health required to divide
HEALTH_TO_PROCREATE = 13  # 38

# how much health is consumed by metabolism per day
HEALTH_DAILY_METABOLISM = 24  # 75

'''
Field parameters.
'''
MAX_POPULATION_COUNT = 100