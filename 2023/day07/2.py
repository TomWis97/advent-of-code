from base import AoCBase
b = AoCBase()
b.parse_args()

card_strength_map = {}
for strength, card in enumerate('AKQT98765432J'[::-1]):
    card_strength_map[card] = str(hex(strength)[-1])
b.debug("card_strength_map:", card_strength_map)

# Sorting hands per type:
# Keys: five, four, full, three, two, one, high
# Each key is a list of strings (the hands)

hands_types = {'five': [], 'four': [], 'full': [],'three': [],
               'two': [], 'one': [], 'high': []}

# Bids is a lookup for the bid of the card.
bids = {}

for hand_raw in b.source_data:
    hand, bid = hand_raw.split(' ')
    if hand in bids:
        raise RuntimeError("Duplicate hand!")
    else:
        bids[hand] = bid
    b.debug("Hand: '{}'".format(hand))
    groups = [] 
    current_card = ''
    current_group = []
    jokers = hand.count('J')
    hand_without_jokers = hand.replace('J', '')
    for index, card in enumerate(sorted(hand_without_jokers)):
        if current_card == '':
            # First card
            current_card = card
            current_group.append(card)
        elif card == current_card:
            current_group.append(card)
        elif card != current_card:
            groups.append(current_group.copy())
            current_group = [card,]
            current_card = card
        if index == len(hand_without_jokers)-1:
            # Last card, cleaning up.
            groups.append(current_group.copy())
            current_group = []
            current_card = ''
    groups.sort(key=len, reverse=True)
    try:
        groups[0].extend(['J'] * jokers)
    except IndexError:
        # Hand is all jokers, so no groups.
        groups.append(['J'] * 5)
    b.debug("Hand {} had groups:".format(hand), groups)

    # Let's categorize this hand.
    if len(groups) == 5:
        # All different cards; high card.
        hands_types['high'].append(hand)
        b.debug("Hand type: high")
    elif len(groups) == 4:
        # Two cards have the same label.
        hands_types['one'].append(hand)
        b.debug("Hand type: one")
    elif len(groups) == 3 and len(groups[0]) == 2 and len(groups[1]) == 2:
        hands_types['two'].append(hand)
        b.debug("Hand type: two")
    elif len(groups) == 3 and len(groups[0]) == 3:
        hands_types['three'].append(hand)
        b.debug("Hand type: three")
    elif len(groups) == 2 and len(groups[0]) == 3 and len(groups[1]) == 2:
        hands_types['full'].append(hand)
        b.debug("Hand type: full")
    elif len(groups) == 2 and len(groups[0]) == 4:
        hands_types['four'].append(hand)
        b.debug("Hand type: four")
    elif len(groups) == 1 and len(groups[0]) == 5:
        hands_types['five'].append(hand)
        b.debug("Hand type: five")
    else:
        raise RuntimeError("Hand {} could not be categorized!".format(hand))

sorted_hands = []
for current_type in ['high', 'one', 'two', 'three', 'full', 'four', 'five']:
    # We're converting hands to integer scores, but we need to able to retrieve
    # the hands back again for looking up bids.
    current_type_converted_values = {} 
    current_type_ranks = []
    for hand_in_category in hands_types[current_type]:
        current_hand = []
        # Convert hand to values
        for card in hand_in_category:
            current_hand.append(card_strength_map[card])
        current_hand_str = ''.join([ str(x) for x in current_hand])
        current_type_converted_values[''.join(current_hand_str)] = hand_in_category
        current_type_ranks.append(''.join(current_hand_str))

    # We've now converted all cards to a string of integers within current_type_ranks
    # and we've stored the relevant hands in current_type_converted_values.
    current_type_ranks.sort(reverse=False)
    for hand_int in current_type_ranks:
        sorted_hands.append(current_type_converted_values[hand_int])
    b.debug("current_type_converted_values", current_type_converted_values)

b.debug("Sorted hands:", sorted_hands)

total_winnings = 0
for index, hand in enumerate(sorted_hands):
    total_winnings += int(bids[hand]) * (index + 1)

print(total_winnings)
