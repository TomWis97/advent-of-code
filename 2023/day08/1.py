from base import AoCBase
b = AoCBase()
b.parse_args()

instructions = [x for x in b.source_data[0]]

b.debug("Instructions:", instructions)

# Dictionary of nodes. Key is source, value is tuple with (left,right).
nodes = {}
for node in b.source_data[2:]:
    source, choices = [ x.strip() for x in node.split('=') ]
    parsed_choices = [ x.strip() for x in choices.replace('(', '').replace(')', '').split(',') ]
    nodes[source] = (parsed_choices[0], parsed_choices[1])
    b.debug("Parsed node '{}' to source = {}, choices =".format(node, source), nodes[source])

steps = 0
current_node = 'AAA'
while not current_node == 'ZZZ':
    step_to_take = instructions[steps % len(instructions)]
    if step_to_take == 'L':
        current_node = nodes[current_node][0]
    elif step_to_take == 'R':
        current_node = nodes[current_node][1]
    else:
        raise ValueError('Unknown step:', step_to_take)
    steps += 1
print(steps)
