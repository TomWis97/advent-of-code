with open('input.txt', 'rt') as f:
    source_data_raw = f.readlines()

source_data = [ x.strip() for x in source_data_raw ]

debugging = False
def debug(*kargs):
    if debugging:
        print(*kargs)

show_progress = True
def progress(*kargs, update=False):
    if show_progress:
        if update:
            print('\r', *kargs, end='', sep='', flush=True)
        else:
            print(*kargs)
            

def translate(source, value):
    """Translate a value through maps.
    Arguments: source is type (i.e. seeds), value (int).
    Returns tuple: (new type, new value)"""
    for found_map in maps[source]['mappings']:
        #debug("Check if {} is in range:".format(value), list(range(found_map['src_range'], found_map['src_range'] + found_map['length'])))
        if value in range(found_map['src_range'], found_map['src_range'] + found_map['length']):
            offset = value - found_map['src_range']
            result_translation = found_map['dest_range'] + offset
            debug("Translate {} to {}. Value {} to {}".format(
                source,
                maps[source]['destination'],
                value,
                result_translation))
            return (maps[source]['destination'], result_translation)
    # No hits.
    debug("Translate {} to {}. No mapping found, value {}".format(
        source,
        maps[source]['destination'],
        value))
    return (maps[source]['destination'], value)

def do_full_translation(source, value):
    destination, result = translate(source, value)
    if destination == 'location':
        return result
    # Yay, recursive.
    return do_full_translation(destination, result)

# maps is a dict with: key is source type.
# value is a dict, with the following structure:
#   'destination' -> string, destination type of map.
#   'mappings' -> list of dicts.
#   - 'src_range' -> int
#   - 'dest_range' -> int
#   - 'length' -> int
maps = {}

current_type = ()
discovered_maps = []
seeds = []
current_line_number = 0
for line in source_data:
    current_line_number += 1
    if line.startswith('seeds: '):
        current_seed_start = None
        for seed_input in [ int(seed) for seed in line.split(':')[1].strip().split(' ') ]:
            if current_seed_start == None:
                current_seed_start = int(seed_input)
            else:
                # current_seed_start is set.
                progress("Building seed list with start={}, length={}".format(current_seed_start, seed_input))
                seeds.extend(range(current_seed_start, current_seed_start + int(seed_input)))
                current_seed_start = None
        debug("Seeds:", seeds)
    elif line == "" or current_line_number == len(source_data):
        if len(discovered_maps) == 0:
            # First whitespace. Ignore.
            debug("Ignoring line as it's the first empty line.")
            continue
        maps[current_type[0]] = {
            'destination': current_type[1],
            'mappings': discovered_maps.copy()}
        debug("Empty line found, saving and resetting vars.")
        current_type = ()
        discovered_maps = []
    elif line[0].isnumeric():
        # Mapping found.
        discovered_maps.append({
            'src_range': int(line.split(' ')[1]),
            'dest_range': int(line.split(' ')[0]),
            'length': int(line.split(' ')[2])})
    else: 
        # Line with description found.
        description = line.split(' ')[0].split('-')
        debug("Current type:", description[0], description[2])
        current_type = (description[0], description[2])

debug("Discovered maps", maps)

# locations is a dict with location as key and seed as value.
locations = {}
amount_of_seeds = len(seeds)
progress("Processing {} seeds.".format(amount_of_seeds))
for index, seed in enumerate(seeds):
    if index % 10000 == 0:
        progress("Processing seeds ({}%)...".format(round(index / amount_of_seeds * 100, 2)), update=True)
    seed_location = do_full_translation('seed', seed)
    locations[seed_location] = seed
    debug("=== Output found: seed {} to location {}".format(
        seed,
        seed_location))

for location, seed in locations.items():
    debug("Seed {} @ location {}".format(seed, location))

progress()
print(sorted(locations.keys())[0])
