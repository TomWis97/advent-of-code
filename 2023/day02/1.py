with open('input.txt', 'rt') as f:
    source_data = f.readlines()

# Parameters
max_red = 12
max_green = 13
max_blue = 14

# Parse data
valid_games = []
for game in source_data:
    valid_game = True
    game_number = game.split(':')[0].split(' ')[-1]
    for subset in game.split(':')[1].split(';'):
        for field in subset.split(','):
            # Detect color
            if field.strip().endswith('red'):
                if int(field.strip().split(' ')[0].strip()) > max_red: valid_game = False
            elif field.strip().endswith('green'):
                if int(field.strip().split(' ')[0].strip()) > max_green: valid_game = False
            elif field.strip().endswith('blue'):
                if int(field.strip().split(' ')[0].strip()) > max_blue: valid_game = False
            else:
                print(subset)
                print("'{}'".format(field))
                raise ValueError("No color detected!")
    if valid_game:
        valid_games.append(game_number)
print(sum([int(x) for x in valid_games]))
