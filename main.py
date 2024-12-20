import player
import deck
import deal
from constants import Better
import random
import calculate
from tqdm import tqdm

def compare_special():
    def will_p1_jam(num_iterations): # p1 has community ability, thus they jam if their hand is good on this river > 50% against ATC
        won_rivers = 0
        for i in range(num_iterations):
            copied = live_deck.deck[:]
            community_cards = set(deal.deal_flop(copied)) | set(deal.deal_turn(copied)) | set(deal.deal_river(copied))
            random.shuffle(copied)
            mock_p = player.Player("Mock")
            mock_p.hole_cards = set([copied.pop(), copied.pop()])
            p1_best = calculate.calculate_hand(p1.hole_cards | community_cards)[1]
            mock_best = calculate.calculate_hand(mock_p.hole_cards | community_cards)[1]
            better_hand = calculate.calculate_better_hand(p1_best, mock_best)[0]
            if better_hand == Better.FIRST_HAND_IS_BETTER:
                won_rivers += 1

        if won_rivers / num_iterations > 0.5:
            return True
        return False


    def will_p2_jam(num_iterations): # p2 has seeing opp cards ability, thus they jam if their hand beats opp hand > 50% on any board
        won_rivers = 0
        opp_hand = p1.hole_cards
        for i in range(num_iterations):
            copied = live_deck.deck[:]
            random.shuffle(copied)
            community_cards = set(deal.deal_flop(copied)) | set(deal.deal_turn(copied)) | set(deal.deal_river(copied))
            p2_best = calculate.calculate_hand(p2.hole_cards | community_cards)[1]
            opp_best = calculate.calculate_hand(p1.hole_cards | community_cards)[1]
            better_hand = calculate.calculate_better_hand(opp_best, p2_best)[0]
            if better_hand == Better.SECOND_HAND_IS_BETTER:
                won_rivers += 1
        if won_rivers / num_iterations > 0.5:
            return True
        return False

    ITERATIONS = 1000
    SUB_ITERATIONS = 100
    p1_won_rivers = 0
    p2_won_rivers = 0
    ties = 0
    played = 0
    for i in tqdm(range(ITERATIONS)):
        p1 = player.Player("Phil Hellmuth")
        p2 = player.Player("Tom Dwan")
        players = []
        players.append(p1)
        players.append(p2)
        live_deck = deck.Deck()
        deal.deal_hole_cards(live_deck.deck, players)
        p1_jams = False
        p2_jams = False
        p1_jams = will_p1_jam(SUB_ITERATIONS)
        if not p1_jams:
            continue
        p2_jams = will_p2_jam(SUB_ITERATIONS)
        if not p2_jams:
            continue
        community_cards = set(deal.deal_flop(live_deck.deck)) | set(deal.deal_turn(live_deck.deck)) | set(deal.deal_river(live_deck.deck))

        played += 1
        p1_best = calculate.calculate_hand(p1.hole_cards | community_cards)[1]
        p2_best = calculate.calculate_hand(p2.hole_cards | community_cards)[1]
        better_hand = calculate.calculate_better_hand(p1_best, p2_best)[0]

        if better_hand == Better.FIRST_HAND_IS_BETTER:
            p1_won_rivers += 1
        elif better_hand == Better.SECOND_HAND_IS_BETTER:
            p2_won_rivers += 1
        else:
            ties += 1
        
    if played > 0:
        print("P1 wins: ", p1_won_rivers)
        print("P2 wins: ", p2_won_rivers)
        print("Tied wins: ", ties)
    else:
        print("No hands showed down")

if __name__ == '__main__':
    pass