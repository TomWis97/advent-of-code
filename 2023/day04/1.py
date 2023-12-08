with open('input.txt', 'rt') as f:
    source_data_raw = f.readlines()

source_data = [ x.strip() for x in source_data_raw ]

debugging = False
def debug(*kargs):
    if debugging:
        print(*kargs)

total_points = 0
for card in source_data:
    card_number = card.split(' ')[1]
    winning_numbers = [ x for x in card.split(':')[1].split('|')[0].strip().split(' ') if x ]
    have_numbers = [ x for x in card.split(':')[1].split('|')[1].strip().split(' ') if x]
    debug("Winning:", winning_numbers)
    debug("Have:", have_numbers)
    wins = [ x for x in have_numbers if x in winning_numbers ]
    debug("Wins:", wins)
    if len(wins) > 0:
        points = 2 ** (len(wins) - 1)
        debug("Points:", points)
        total_points += points
print(total_points)
