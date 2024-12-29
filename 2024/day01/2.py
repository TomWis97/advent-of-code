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

score = 0
for x in list1:
    times = 0
    for y in list2:
        if x == y:
            times += 1
    score += times * x
print(score)
