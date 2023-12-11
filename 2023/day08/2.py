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
current_nodes_list = [ x for x in nodes.keys() if x.endswith('A') ]
b.debug("Starting with nodes:", current_nodes_list)

while not all([y.endswith('Z') for y in current_nodes_list]):
    for node_index, node in enumerate(current_nodes_list):
        step_to_take = instructions[steps % len(instructions)]
        if step_to_take == 'L':
            current_nodes_list[node_index] = nodes[current_nodes_list[node_index]][0]
        elif step_to_take == 'R':
            current_nodes_list[node_index] = nodes[current_nodes_list[node_index]][1]
        else:
            raise ValueError('Unknown step:', step_to_take)
    steps += 1
    b.debug("Current state of nodes:", current_nodes_list)
    if steps % 1000000 == 0:
        b.progress("Currenty at {} steps.".format(steps))
print(steps)
