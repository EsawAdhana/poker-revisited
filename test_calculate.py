import unittest
from constants import Suits, Numbers, Hand
from engine import compare_evaluators
import calculate
from deck import Deck
import deck
import deal
import player
import time

def speed_check(iterations=100_000):
    print("Running speed check")
    start = time.time()
    for i in range(iterations):
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
        _, _ = calculate.calculate_better_hand(p1_best, p2_best)
    end = time.time()
    print(f"Execution time: {(end - start):.4f} seconds")

class PokerHandTests(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def assert_hand(self, cards, expected_score):
        score, best_hand = calculate.calculate_hand(cards)
        self.assertEqual(score, expected_score)
        self.assertEqual(set(best_hand), set(cards[:5]))

    def test_RF_basic(self):
        royal_flush = [
            self.deck.Card(Suits.CLUBS.value, Numbers.ACE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.KING.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.QUEEN.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.JACK.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.TEN.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.HEARTS.value, Numbers.THREE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.TWO.value)
        ]
        self.assert_hand(royal_flush + extra_cards, Hand.ROYAL_FLUSH)

    def test_RF_with_lower_SF(self):
        royal_flush = [
            self.deck.Card(Suits.CLUBS.value, Numbers.ACE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.KING.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.QUEEN.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.JACK.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.TEN.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.CLUBS.value, Numbers.NINE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.EIGHT.value)
        ]
        self.assert_hand(royal_flush + extra_cards, Hand.ROYAL_FLUSH)

    def test_SF_basic(self):
        straight_flush = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.KING.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.QUEEN.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.JACK.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TEN.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.NINE.value),
        ]
        extra_cards = [
            self.deck.Card(Suits.CLUBS.value, Numbers.THREE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.TWO.value)
        ]
        self.assert_hand(straight_flush + extra_cards, Hand.STRAIGHT_FLUSH)

    def test_SF_with_lower_SF(self):
        straight_flush = [
            self.deck.Card(Suits.SPADES.value, Numbers.KING.value),
            self.deck.Card(Suits.SPADES.value, Numbers.QUEEN.value),
            self.deck.Card(Suits.SPADES.value, Numbers.JACK.value),
            self.deck.Card(Suits.SPADES.value, Numbers.TEN.value),
            self.deck.Card(Suits.SPADES.value, Numbers.NINE.value),
        ]
        extra_cards = [
            self.deck.Card(Suits.SPADES.value, Numbers.EIGHT.value),
            self.deck.Card(Suits.SPADES.value, Numbers.SEVEN.value)
        ]
        self.assert_hand(straight_flush + extra_cards, Hand.STRAIGHT_FLUSH)

    def test_SF_with_NF(self):
        straight_flush = [
            self.deck.Card(Suits.HEARTS.value, Numbers.QUEEN.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.JACK.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.TEN.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.NINE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.EIGHT.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.HEARTS.value, Numbers.ACE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value)
        ]
        self.assert_hand(straight_flush + extra_cards, Hand.STRAIGHT_FLUSH)

    def test_SF_with_A_low(self):
        straight_flush = [
            self.deck.Card(Suits.HEARTS.value, Numbers.ACE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.TWO.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.THREE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.FOUR.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.FIVE.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.ACE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value)
        ]
        self.assert_hand(straight_flush + extra_cards, Hand.STRAIGHT_FLUSH)

    def test_4K_basic(self):
        four_of_a_kind = [
            self.deck.Card(Suits.CLUBS.value, Numbers.ACE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.ACE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.ACE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.ACE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.KING.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.CLUBS.value, Numbers.THREE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.TWO.value)
        ]
        self.assert_hand(four_of_a_kind + extra_cards, Hand.FOUR_OF_A_KIND)

    def test_4K_with_FH(self):
        four_of_a_kind = [
            self.deck.Card(Suits.CLUBS.value, Numbers.ACE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.ACE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.ACE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.ACE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.KING.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.KING.value),
            self.deck.Card(Suits.SPADES.value, Numbers.KING.value)
        ]
        self.assert_hand(four_of_a_kind + extra_cards, Hand.FOUR_OF_A_KIND)
    
    def test_FH_basic(self):
        full_house = [
            self.deck.Card(Suits.CLUBS.value, Numbers.ACE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.ACE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.ACE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.KING.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.KING.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.SPADES.value, Numbers.THREE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value)
        ]
        self.assert_hand(full_house + extra_cards, Hand.FULL_HOUSE)
        
    def test_FH_basic(self):
        full_house = [
            self.deck.Card(Suits.CLUBS.value, Numbers.ACE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.ACE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.ACE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.KING.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.KING.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.SPADES.value, Numbers.THREE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value)
        ]
        self.assert_hand(full_house + extra_cards, Hand.FULL_HOUSE)

    def test_FH_with_lower_FH(self):
        full_house = [
            self.deck.Card(Suits.CLUBS.value, Numbers.THREE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.THREE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.THREE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.TWO.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.TWO.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value),
            self.deck.Card(Suits.SPADES.value, Numbers.TEN.value)
        ]
        self.assert_hand(full_house + extra_cards, Hand.FULL_HOUSE)

    def test_F_basic(self):
        flush = [
            self.deck.Card(Suits.SPADES.value, Numbers.ACE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.KING.value),
            self.deck.Card(Suits.SPADES.value, Numbers.QUEEN.value),
            self.deck.Card(Suits.SPADES.value, Numbers.JACK.value),
            self.deck.Card(Suits.SPADES.value, Numbers.NINE.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.EIGHT.value),
            self.deck.Card(Suits.SPADES.value, Numbers.SEVEN.value)
        ]
        self.assert_hand(flush + extra_cards, Hand.FLUSH)

    def test_F_with_straight(self):
        flush = [
            self.deck.Card(Suits.SPADES.value, Numbers.KING.value),
            self.deck.Card(Suits.SPADES.value, Numbers.QUEEN.value),
            self.deck.Card(Suits.SPADES.value, Numbers.JACK.value),
            self.deck.Card(Suits.SPADES.value, Numbers.TEN.value),
            self.deck.Card(Suits.SPADES.value, Numbers.EIGHT.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.ACE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.NINE.value)
        ]
        self.assert_hand(flush + extra_cards, Hand.FLUSH)

    def test_S_basic(self):
        straight = [
            self.deck.Card(Suits.CLUBS.value, Numbers.ACE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.KING.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.QUEEN.value),
            self.deck.Card(Suits.SPADES.value, Numbers.JACK.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.TEN.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.CLUBS.value, Numbers.THREE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.TWO.value)
        ]
        self.assert_hand(straight + extra_cards, Hand.STRAIGHT)

    def test_S_with_A_low(self):
        straight = [
            self.deck.Card(Suits.CLUBS.value, Numbers.ACE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.THREE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.FOUR.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.FIVE.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.HEARTS.value, Numbers.KING.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.KING.value)
        ]
        self.assert_hand(straight + extra_cards, Hand.STRAIGHT)

    def test_S_with_lower_S(self):
        straight = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.THREE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.FOUR.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.FIVE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.SIX.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.HEARTS.value, Numbers.ACE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.KING.value)
        ]
        self.assert_hand(straight + extra_cards, Hand.STRAIGHT)

    def test_3K_basic(self):
        three_of_a_kind = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.ACE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.ACE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.ACE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.KING.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.QUEEN.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.HEARTS.value, Numbers.THREE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value)
        ]
        self.assert_hand(three_of_a_kind + extra_cards, Hand.THREE_OF_A_KIND)

    def test_3K_basic(self):
        three_of_a_kind = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.ACE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.ACE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.ACE.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.KING.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.QUEEN.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.HEARTS.value, Numbers.THREE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value)
        ]
        self.assert_hand(three_of_a_kind + extra_cards, Hand.THREE_OF_A_KIND)

    def test_2P_basic(self):
        two_pair = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.ACE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.ACE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.KING.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.KING.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.QUEEN.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.HEARTS.value, Numbers.THREE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value)
        ]
        self.assert_hand(two_pair + extra_cards, Hand.TWO_PAIR)

    def test_1P_basic(self):
        one_pair = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.ACE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.ACE.value),
            self.deck.Card(Suits.SPADES.value, Numbers.KING.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.QUEEN.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.JACK.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.HEARTS.value, Numbers.THREE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value)
        ]
        self.assert_hand(one_pair + extra_cards, Hand.ONE_PAIR)

    def test_HC_basic(self):
        high_card = [
            self.deck.Card(Suits.DIAMONDS.value, Numbers.ACE.value),
            self.deck.Card(Suits.HEARTS.value, Numbers.KING.value),
            self.deck.Card(Suits.SPADES.value, Numbers.QUEEN.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.JACK.value),
            self.deck.Card(Suits.CLUBS.value, Numbers.NINE.value)
        ]
        extra_cards = [
            self.deck.Card(Suits.HEARTS.value, Numbers.THREE.value),
            self.deck.Card(Suits.DIAMONDS.value, Numbers.TWO.value)
        ]
        self.assert_hand(high_card + extra_cards, Hand.HIGH_CARD)


if __name__ == '__main__':
    # compare_evaluators()
    # unittest.main()
    speed_check()