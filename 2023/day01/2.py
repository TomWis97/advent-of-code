with open('input.txt', 'rt') as f:
    source_data = f.readlines()

number_dict = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9}

numbers = []
for line in source_data:
    numbers_in_line = []
    for index in range(0, len(line)):
        processing = line[index:]
        try:
            numbers_in_line.append(int(processing[0]))
            continue
        except:
            pass
        for translation_word, translation_number in number_dict.items():
            if processing.startswith(translation_word):
                numbers_in_line.append(translation_number)
    number = int(str(numbers_in_line[0]) + str(numbers_in_line[-1]))
    numbers.append(number)

total = 0
for number in numbers:
    total += number
print(total)
