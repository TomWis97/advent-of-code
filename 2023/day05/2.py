import uuid
import argparse
import json

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

def process_batch(begin, end, jid):
    lowest = None
    with open('maps.json', 'rt') as f:
        global maps
        maps = json.loads(f.read())
    for index, seed in enumerate(range(begin, end)):
        if index % 1000000 == 0:
            progress("[{}] Processing seeds ({}%)...".format(jid, round(index / (end - begin) * 100, 2)))
        current_location = do_full_translation('seed', seed)
        if lowest == None or current_location < lowest:
            lowest = current_location
    filename = 'results-' + str(uuid.uuid4()) + '.json'
    with open(filename, 'wt') as f:
        print(lowest)
        f.write(json.dumps(lowest))

def parse_input():
    """Writes maps.json
    Writes seeds to stdout."""
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
                    seeds.extend((current_seed_start, current_seed_start + int(seed_input)))
                    print(current_seed_start, current_seed_start + int(seed_input))
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
    with open('maps.json', 'wt') as f:
        f.write(json.dumps(maps))

def parse_results(filenames):
    result_list = []
    for file in filenames:
        with open(file, 'rt') as f:
            result_list.append(int(f.read()))
    return sorted(result_list)[0]

def process():
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    parser_input = subparsers.add_parser('read_input',
                                         help='Parse the input.txt file')

    parser_process = subparsers.add_parser('process',
                                           help='process input')
    parser_process.add_argument('start', help="start parameter", type=int)
    parser_process.add_argument('end', help="end parameter", type=int)
    parser_process.add_argument('jid', help="job id", type=int)

    parser_result = subparsers.add_parser('results',
                                          help='parse result files')
    parser_result.add_argument('input', action='store', nargs='+')
    
    arguments = parser.parse_args()

    if arguments.command == 'read_input':
        show_progress = False
        parse_input()
    elif arguments.command == 'process':
        process_batch(arguments.start, arguments.end, arguments.jid)
    elif arguments.command == 'results':
        print(parse_results(arguments.input))
