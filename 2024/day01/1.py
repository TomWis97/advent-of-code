from base import AoCBase
b = AoCBase()
b.parse_args()

list1 = []
list2 = []
for line in b.source_data:
    item1, item2 = [ int(x.strip()) for x in line.split(' ') if x.strip() != "" ]
    list1.append(item1)
    list2.append(item2)

list1.sort()
list2.sort()

b.debug("List 1:", list1)
b.debug("List 2:", list2)

total_difference = 0
for x in range(len(b.source_data)):
    difference = abs(list1[x] - list2[x])
    b.debug("{} - {} = {}".format(list1[x], list2[x], difference))
    total_difference += difference

print(total_difference)

