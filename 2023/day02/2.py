with open('input.txt', 'rt') as f:
    source_data = f.readlines()

# Parse data
all_powers = []
for game in source_data:
    #print("Game:", game.strip())
    least_cubes = {
            'red': 0,
            'green': 0,
            'blue': 0}
    valid_game = True
    game_number = game.split(':')[0].split(' ')[-1]
    for subset in game.split(':')[1].split(';'):
        for field in subset.split(','):
            # Detect color
            for colour in ['red', 'green', 'blue']:
                if field.strip().endswith(colour):
                    amount = int(field.strip().split(' ')[0])
                    if least_cubes[colour] < amount:
                        least_cubes[colour] = amount
    #print("least_cubes", least_cubes, end="\n\n")
    all_powers.append(least_cubes['red'] * least_cubes['green'] * least_cubes['blue'])
print(sum(all_powers))
