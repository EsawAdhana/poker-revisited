from phevaluator.evaluator import evaluate_cards
from constants import Suits, Numbers, Better
from itertools import combinations
import calculate
from deck import Deck
import deck
import deal
import player
from tqdm import tqdm

def convert_to_phevaluator_format(card):
    rank_map = {14: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T'}
    suit_map = {
        Suits.CLUBS: 'c',
        Suits.DIAMONDS: 'd',
        Suits.HEARTS: 'h',
        Suits.SPADES: 's'
    }
    rank = str(card.value) if card.value < 10 else rank_map[card.value]
    suit = suit_map[card.suit]
    return f"{rank}{suit}"

def convert_from_phevaluator_format(card_str):
    rank_map = {'A': Numbers.ACE, 'K': Numbers.KING, 
                'Q': Numbers.QUEEN, 'J': Numbers.JACK, 
                'T': Numbers.TEN}
    suit_map = {'c': Suits.CLUBS, 'd': Suits.DIAMONDS, 
                'h': Suits.HEARTS, 's': Suits.SPADES}
    
    rank = Numbers(int(card_str[0])) if card_str[0].isdigit() else rank_map[card_str[0]]
    suit = suit_map[card_str[1]]
    return Deck.Card(suit, rank)

def get_best_hand_phevaluator(cards):
    ph_cards = [convert_to_phevaluator_format(card) for card in cards]
    best_score = float('inf')
    best_hand = None
    for combo in combinations(ph_cards, 5):
        score = evaluate_cards(*combo)
        if score < best_score:
            best_score = score
            best_hand = combo
    return best_score, best_hand

def compare_evaluators(num_tests=100_000):
    matches = 0
    mismatches = 0

    for _ in tqdm(range(num_tests)):
        players = []
        p1 = player.Player("P1")
        p2 = player.Player("P2")
        players.append(p1)
        players.append(p2)
        live_deck = deck.Deck()
        deal.deal_hole_cards(live_deck.deck, players)

        community_cards = set(deal.deal_flop(live_deck.deck)) | set(deal.deal_turn(live_deck.deck)) | set(deal.deal_river(live_deck.deck))

        p1_best = calculate.calculate_hand(p1.hole_cards | community_cards)[1]
        p2_best = calculate.calculate_hand(p2.hole_cards | community_cards)[1]
        score, _ = calculate.calculate_better_hand(p1_best, p2_best)
        if score == Better.SECOND_HAND_IS_BETTER:
            best = calculate.calculate_hand(p2_best)[1]
        else:
            best = calculate.calculate_hand(p1_best)[1]

        p1_score, bh1 = get_best_hand_phevaluator(p1.hole_cards | community_cards)
        p2_score, bh2 = get_best_hand_phevaluator(p2.hole_cards | community_cards)
        
        if p1_score < p2_score:
            best_hand = bh1
            ph_result = Better.FIRST_HAND_IS_BETTER
        elif p2_score < p1_score:
            ph_result = Better.SECOND_HAND_IS_BETTER
            best_hand = bh2
        else:
            ph_result = Better.TIE
            best_hand = bh1

        best_hand = [convert_from_phevaluator_format(card) for card in best_hand]
        if score == ph_result:
            matches += 1
        else:
            mismatches += 1
            print(f"Mismatch found:")
            print(f"P1 hole cards: {[str(card) for card in p1.hole_cards]}")
            print(f"P2 hole cards: {[str(card) for card in p2.hole_cards]}")
            print(f"Community cards: {[str(card) for card in community_cards]}")
            print(f"Your best: {best}")
            print(f"phev best: {best_hand}")
            print(f"Your better hand: {score}")
            print(f"True better hand: {ph_result}")
            print()

    print(f"Total tests: {num_tests}")
    print(f"Matches: {matches}")
    print(f"Mismatches: {mismatches}")
    print(f"Accuracy: {matches / num_tests * 100:.2f}%")