from constants import Better, Hand
from itertools import combinations
from collections import defaultdict


def calculate_hand(total_cards):
    best_hand = []
    SCORE = 0
    for combo in combinations(total_cards, 5):
        if not SCORE:
            best_hand, SCORE = combo, calculate_combo(combo)
        else:
            better_hand_check, new_score = calculate_better_hand(best_hand, combo)
            if better_hand_check == Better.SECOND_HAND_IS_BETTER:
                best_hand = combo
                SCORE = new_score

    return SCORE, best_hand

def calculate_better_hand(first, second):
    calc_first = calculate_combo(first)
    calc_second = calculate_combo(second)
    if calc_first < calc_second:
        return Better.FIRST_HAND_IS_BETTER, calc_first
    elif calc_first > calc_second:
        return Better.SECOND_HAND_IS_BETTER, calc_second
    else:
        if calc_first == calc_second: # Will always be true at this point
            if calc_first == Hand.ROYAL_FLUSH:
                return Better.TIE, calc_first
            elif calc_first == Hand.STRAIGHT_FLUSH:
                better, hand = compare_straight_flush(first, second)
            elif calc_first == Hand.FOUR_OF_A_KIND:
                better, hand = compare_four_of_a_kind(first, second)
            elif calc_first == Hand.FULL_HOUSE:
                better, hand = compare_full_house(first, second)
            elif calc_first == Hand.FLUSH:
                better, hand = compare_high_cards(first, second)
            elif calc_first == Hand.STRAIGHT:
                better, hand = compare_straight(first, second)
            elif calc_first == Hand.THREE_OF_A_KIND:
                better, hand = compare_three_of_a_kind(first, second)
            elif calc_first == Hand.TWO_PAIR:
                better, hand = compare_two_pair(first, second)
            elif calc_first == Hand.ONE_PAIR:
                better, hand = compare_one_pair(first, second)
            else:
                better, hand = compare_high_cards(first, second)
            return better, hand

def compare_straight_flush(first, second):
    return compare_straight(first, second) # Same process, since the flush part doesn't matter here

def compare_four_of_a_kind(first, second):
    first_num_freq = get_num_freq(first)
    second_num_freq = get_num_freq(second)
    
    for key, val in first_num_freq.items():
        if val == 4:
            first_4K_4 = key
        elif val == 1:
            first_4K_1 = key

    for key, val in second_num_freq.items():
        if val == 4:
            second_4K_4 = key
        elif val == 1:
            second_4K_1 = key

    if second_4K_4 > first_4K_4:
        return Better.SECOND_HAND_IS_BETTER, calculate_combo(second)
    elif second_4K_4 < first_4K_4:
        return Better.FIRST_HAND_IS_BETTER, calculate_combo(first)
    else:
        if second_4K_1 > first_4K_1:
            return Better.SECOND_HAND_IS_BETTER, calculate_combo(second)
        elif second_4K_1 < first_4K_1:
            return Better.FIRST_HAND_IS_BETTER, calculate_combo(first)
        else:
            return Better.TIE, calculate_combo(first) 

def compare_full_house(first, second):
    first_num_freq = get_num_freq(first)
    second_num_freq = get_num_freq(second)
    
    for key, val in first_num_freq.items():
        if val == 3:
            first_FH_3 = key
        elif val == 2:
            first_FH_2 = key
    for key, val in second_num_freq.items():
        if val == 3:
            second_FH_3 = key
        elif val == 2:
            second_FH_2 = key
    if second_FH_3 > first_FH_3:
        return Better.SECOND_HAND_IS_BETTER, calculate_combo(second)
    elif second_FH_3 < first_FH_3:
        return Better.FIRST_HAND_IS_BETTER, calculate_combo(first)
    else:
        if second_FH_2 > first_FH_2:
            return Better.SECOND_HAND_IS_BETTER, calculate_combo(second)
        elif second_FH_2 < first_FH_2:
            return Better.FIRST_HAND_IS_BETTER, calculate_combo(first)
        else:
            return Better.TIE, calculate_combo(first)
        
def compare_flush(first, second):
    return compare_high_cards(first, second) # Same process, just interested in ranking of cards by value now

def compare_straight(first, second):
    def get_straight_value(hand):
        values = sorted([card.value for card in hand])
        if values == [2, 3, 4, 5, 14]:  # Ace-low straight
            return 5
        return max(values)

    first_value = get_straight_value(first)
    second_value = get_straight_value(second)

    if second_value > first_value:
        return Better.SECOND_HAND_IS_BETTER, calculate_combo(second)
    elif first_value > second_value:
        return Better.FIRST_HAND_IS_BETTER, calculate_combo(first)
    else:
        return Better.TIE, calculate_combo(first)

def compare_three_of_a_kind(first, second):
    first_num_freq = get_num_freq(first)
    second_num_freq = get_num_freq(second)
    
    for key, val in first_num_freq.items():
        if val == 3:
            first_3K = key
    for key, val in second_num_freq.items():
        if val == 3:
            second_3K = key
    if second_3K > first_3K:
        return Better.SECOND_HAND_IS_BETTER, calculate_combo(second)
    elif second_3K < first_3K:
        return Better.FIRST_HAND_IS_BETTER, calculate_combo(first)
    else:
        return compare_high_cards(first, second)
    
def compare_two_pair(first, second):
    first_num_freq = get_num_freq(first)
    second_num_freq = get_num_freq(second)
    first_pairs = []
    second_pairs = []
    for key, val in first_num_freq.items():
        if val == 2:
            first_pairs.append(key)
    for key, val in second_num_freq.items():
        if val == 2:
            second_pairs.append(key)
        
    if max(second_pairs) > max(first_pairs):
        return Better.SECOND_HAND_IS_BETTER, calculate_combo(second)
    elif max(second_pairs) < max(first_pairs):
        return Better.FIRST_HAND_IS_BETTER, calculate_combo(first)
    else:
        if min(second_pairs) > min(first_pairs):
            return Better.SECOND_HAND_IS_BETTER, calculate_combo(second)
        elif min(second_pairs) < min(first_pairs):
            return Better.FIRST_HAND_IS_BETTER, calculate_combo(first)
        else:
            return compare_high_cards(first, second)
        
def compare_one_pair(first, second):
    first_num_freq = get_num_freq(first)
    second_num_freq = get_num_freq(second)

    for key, val in first_num_freq.items():
        if val == 2:
            first_1P = key
    for key, val in second_num_freq.items():
        if val == 2:
            second_1P = key
    if second_1P > first_1P:
        return Better.SECOND_HAND_IS_BETTER, calculate_combo(second)
    elif second_1P < first_1P:
        return Better.FIRST_HAND_IS_BETTER, calculate_combo(first)
    else:
        return compare_high_cards(first, second)

def compare_high_cards(first, second):
    sorted_first = sorted(first, key=lambda card: card.value, reverse=True)
    sorted_second = sorted(second, key=lambda card: card.value, reverse=True)
    for card1, card2 in zip(sorted_first, sorted_second):
        if card1.value < card2.value:
            return Better.SECOND_HAND_IS_BETTER, calculate_combo(second)
        elif card1.value > card2.value:
            return Better.FIRST_HAND_IS_BETTER, calculate_combo(first)
    else:
        # Hands are identical in value (ex. Ac, Ad, Ah, As, Kc vs Ac, Ad, Ah, As, Kd), so can save calculation by returning first (not updating hand)
        return Better.TIE, calculate_combo(first)

def calculate_combo(combo):
    sorted_combo = sorted(combo, key=lambda card: card.value)
    num_freq = get_num_freq(sorted_combo)
    suit_freq = get_suit_freq(sorted_combo)

    if is_royal_flush(sorted_combo, suit_freq, num_freq):
        return Hand.ROYAL_FLUSH
    elif is_straight_flush(sorted_combo, suit_freq, num_freq):
        return Hand.STRAIGHT_FLUSH
    elif is_four_of_a_kind(num_freq):
        return Hand.FOUR_OF_A_KIND
    elif is_full_house(num_freq):
        return Hand.FULL_HOUSE
    elif is_flush(suit_freq):
        return Hand.FLUSH
    elif is_straight(sorted_combo, num_freq):
        return Hand.STRAIGHT
    elif is_three_of_a_kind(num_freq):
        return Hand.THREE_OF_A_KIND
    elif is_two_pair(num_freq):
        return Hand.TWO_PAIR
    elif is_one_pair(num_freq):
        return Hand.ONE_PAIR
    elif is_high_card():
        return Hand.HIGH_CARD
    else:
        raise Exception("Error. Not any possible hand. Something went wrong.")

def is_royal_flush(combo_sorted, suit_freq, num_freq):
    return combo_sorted[0].value == 10 and is_straight_flush(combo_sorted, suit_freq, num_freq)

def is_straight_flush(combo_sorted, suit_freq, num_freq):
    return is_flush(suit_freq) and is_straight(combo_sorted, num_freq) 

def is_four_of_a_kind(num_freq):
    return any(card_freq == 4 for card_freq in num_freq.values())

def is_full_house(num_freq):
    return any(card_freq == 3 for card_freq in num_freq.values()) and any(card_freq == 2 for card_freq in num_freq.values())

def is_flush(suit_freq):
    return any(card_freq == 5 for card_freq in suit_freq.values()) 

def is_straight(combo_sorted, num_freq):
    if num_freq[14] > 0:
        if num_freq[2] > 0 and num_freq[3] > 0 and num_freq[4] > 0 and num_freq[5] > 0: # Ace low
            return True
        if num_freq[10] > 0 and num_freq[11] > 0 and num_freq[12] > 0 and num_freq[13] > 0: # Ace high
            return True

    for i in range(len(combo_sorted) - 1):
        if combo_sorted[i].value + 1 != combo_sorted[i + 1].value:
            return False
    return True
        
def is_three_of_a_kind(num_freq):
    return any(card_freq == 3 for card_freq in num_freq.values())

def is_two_pair(num_freq):
    return sum(card_freq == 2 for card_freq in num_freq.values()) == 2

def is_one_pair(num_freq):
    return any(card_freq == 2 for card_freq in num_freq.values())

def is_high_card():
    return True

def get_num_freq(combo):
    num_freq = defaultdict(int)
    for card in combo:
        num_freq[card.value] += 1
    return num_freq

def get_suit_freq(combo):
    suit_freq = defaultdict(int)
    for card in combo:
        suit_freq[card.suit] += 1 
    return suit_freq

if __name__ == '__main__':
    print("Running a file not intended to be run directly")