with open('input.txt', 'rt') as f:
    source_data_raw = f.readlines()
    source_data = [ x.strip() for x in source_data_raw]

def contains_symbol(input_string):
    """Check if input_string contains a relavant symbol.
    Returns boolean."""
    non_symbols = ["."] + [ str(x) for x in range(0,10) ]
    # If all characters are ".", then output of any will be True.
    # We're checking if any character is NOT in non_symbols. So invert.
    result = False
    for character in input_string:
        if character not in non_symbols:
            result = True
    debug("contains_symbol: ", input_string, result)
    return result

debugging = False
def debug(*kargs):
    if debugging:
        print(*kargs)


# Zero indexed, because Python is zero-indexed.
line_number = 0
all_numbers = []
part_numbers = []
current_number_string = ""
is_part_number = False

for line in source_data:
    character_index = -1  # Index of where we are within the line.
    all_numbers_line = []
    for character in line:
        character_index += 1
        try:
            # If this succeeds, found a number.
            current_number_string = current_number_string + str(int(character))
            if character_index == len(line) - 1:
                # We're at the end of the line.
                debug("End of line detected while finding number.")
            else:
                continue # Continue to next character
        except:
            pass

        if current_number_string != "":
            # We found a complete number.
            debug("Complete number:", current_number_string)
            all_numbers_line.append(int(current_number_string))
            # We need to search in a range 2 chars wider than the length of current_number_string. Because also diagonal.
            start_index = character_index - len(current_number_string) - 1
            end_index = character_index + 1 # One more for diagonal.
            debug("start_index: {}, end_index: {}, len: {}".format(start_index, end_index, len(line)))
            if start_index < 0:
                start_index = 0  # Prevent -1 as start_number.
            if end_index > len(line):
                # We cannot have an end larger than line length.
                end_index = len(line)

            # Begin checking if current_number_string is actually a partnumber.
            # One line above.
            if line_number > 0:
                # Cannot check above first line.
                if contains_symbol(source_data[line_number - 1][start_index:end_index]):
                    is_part_number = True
            # Current line
            if contains_symbol(source_data[line_number][start_index:end_index]):
                # This number is a part number!
                is_part_number = True
            # One line below.
            if line_number < len(source_data) - 1:
                # Cannot check below last line.
                if contains_symbol(source_data[line_number + 1][start_index:end_index]):
                    is_part_number = True
            if is_part_number:
                part_numbers.append(int(current_number_string))
                debug("Part number found: ", int(current_number_string))
            is_part_number = False
            current_number_string = "" # Reset for the next number.
    all_numbers.append(all_numbers_line)
    line_number += 1
debug("Part numbers:", part_numbers)
print(sum(part_numbers))
