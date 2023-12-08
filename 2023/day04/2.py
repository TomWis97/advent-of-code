with open('input.txt', 'rt') as f:
    source_data_raw = f.readlines()

source_data = [ x.strip() for x in source_data_raw ]

debugging = False
def debug(*kargs):
    if debugging:
        print(*kargs)

card_instances = [1] * len(source_data)
current_card = 0

for card in source_data:
    print("===== Card:", card)
    card_number = card.split(' ')[1]
    winning_numbers = [ x for x in card.split(':')[1].split('|')[0].strip().split(' ') if x ]
    have_numbers = [ x for x in card.split(':')[1].split('|')[1].strip().split(' ') if x]
    debug("Winning:", winning_numbers)
    debug("Have:", have_numbers)
    wins = [ x for x in have_numbers if x in winning_numbers ]
    debug("Wins:", wins)
    for x in range(len(wins)):
        print("x = ", x)
        card_instances[current_card + x + 1] += card_instances[current_card]
    debug("card_instances", card_instances)
    current_card += 1
    
print(sum(card_instances))
