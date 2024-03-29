from numpy import sqrt, ceil, floor
with open('input.txt', 'rt') as f:
    source_data_raw = f.readlines()

source_data = [ x.strip() for x in source_data_raw ]

debugging = False
def debug(*kargs):
    if debugging:
        print(*kargs)

times = [ int(x.strip()) for x in source_data[0].split(':')[1].split(' ') if x ]
distances = [ int(x.strip()) for x in source_data[1].split(':')[1].split(' ') if x ]

# List of tuples. Tuple per race: (time, distance)
races = []
for index, time in enumerate(times):
    races.append((time, distances[index]))

debug("Races:", races)

ways_to_win = None
for race in races:
    time = race[0]
    distance = race[1]
    # abc-method. Add 0.001 because it not supposed to be equal, but more or less than.
    lower_limit = (( -abs(time)+sqrt((time ** 2)-(4*-1*-abs(distance)))) / (2*-1)) + 0.001
    upper_limit = (( -abs(time)-sqrt((time ** 2)-(4*-1*-abs(distance)))) / (2*-1)) - 0.001
    debug("Lower limit: {}, rounded: {}".format(lower_limit, ceil(lower_limit)))
    debug("Upper limit: {}, rounded: {}".format(upper_limit, floor(upper_limit)))
    amount_of_ways = int(floor(upper_limit) - ceil(lower_limit) + 1) # Also include first number
    debug("Race has {} ways to win.".format(amount_of_ways))
    if ways_to_win == None:
        ways_to_win = amount_of_ways
    else:
        ways_to_win = ways_to_win * amount_of_ways
print(ways_to_win)
