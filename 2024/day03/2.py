from base import AoCBase
import re

b = AoCBase()
b.parse_args()

regex = re.compile(r"(?<=mul\()\d{1,3},\d{1,3}(?=\))|do\(\)|don't\(\)")
b.debug("Using regex:", regex)
matches = re.findall(regex, ''.join(b.source_data))

b.debug("Found matches:", matches)

enabled_instructions = []
enabled = True
for match in matches:
    if match == "do()":
        enabled = True
        continue
    elif match == "don't()":
        enabled = False
        continue
    if enabled:
        enabled_instructions.append(match)

b.debug("Enabled instructions:", enabled_instructions)
total = 0
for match in enabled_instructions:
    parameters = match.split(',')
    total += int(match.split(',')[0]) * int(match.split(',')[1])
print(total)
