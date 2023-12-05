with open('input.txt', 'rt') as f:
    source_data = f.readlines()

numbers = []
for line in source_data:
    first_number = None
    last_number = None
    for character in line:
        if first_number == None:
            try:
                first_number = int(character)
            except:
                pass
        try:
            last_number = int(character)
        except:
            pass
    number = int(str(first_number) + str(last_number))
    numbers.append(number)

total = 0
for number in numbers:
    total += number
print(total)
