from constants import Numbers, Suits
from statistics import mean
import random

class Deck:
    def __init__(self): 
        self.deck = [
        self.Card(suit, number)
        for suit in Suits
        for number in Numbers
        ]
        random.shuffle(self.deck)
        
    def __str__(self):
        result = "\n".join(str(card) for card in self.deck)
        return result
    
    def gsr_shuffle(self):
        # Ex: [A, B, C, D, E, F, G, H]
        cut_point = self.binomial_cut(len(self.deck)) # After [D] on avg
        left_pile = self.deck[:cut_point] # [A, B, C, D]
        right_pile = self.deck[cut_point:] # [E, F, G, H]

        shuffled_deck = []
        while left_pile or right_pile:
            if not left_pile:
                shuffled_deck.extend(right_pile)
                break
            elif not right_pile:
                shuffled_deck.extend(left_pile)
                break
            else:
                total_cards = len(left_pile) + len(right_pile)
                if random.random() < len(left_pile) / total_cards:
                    shuffled_deck.append(left_pile.pop(0))
                else:
                    shuffled_deck.append(right_pile.pop(0))

        self.deck = shuffled_deck

    def strip_cut_shuffle(self):
        initial_size = len(self.deck)
        min_strip = initial_size // 6
        max_strip = initial_size // 6
        result = []
        while self.deck:
            strip_size = random.randint(min_strip, max_strip)
            if len(self.deck) <= strip_size:
                result = result + self.deck
                break
            else:
                strip = self.deck[-strip_size:]
                result = result + strip
                self.deck = self.deck[:-strip_size]
        self.deck = result
    
    def cut_deck(self):
        # Ex: [A, B, C, D, E, F, G, H]
        cut_point = self.binomial_cut(len(self.deck)) # After [D] on avg
        left_pile = self.deck[:cut_point] # [A, B, C, D]
        right_pile = self.deck[cut_point:] # [E, F, G, H]
        self.deck = right_pile + left_pile # [E, F, G, H, A, B, C, D]

    def binomial_cut(self, n):
        p = 0.5
        return sum(random.random() < p for _ in range(n))

    def shuffle(self):
        self.gsr_shuffle()
        self.gsr_shuffle()
        self.strip_cut_shuffle()
        self.gsr_shuffle()
        self.cut_deck()
        # random.shuffle(self.deck)

    def test_shuffle_distribution(self, num_iterations):
        target_card = Deck.Card(Suits.SPADES.value, Numbers.ACE.value)

        count_in_top_twelve = 0

        for _ in range(num_iterations):
            deck = Deck()
            
            deck.deck.append(target_card)
            deck.shuffle()

            if target_card in deck.deck[-12:]:
                count_in_top_twelve += 1

        likelihood = (count_in_top_twelve / num_iterations) * 100
        
        print(f"Likelihood of Ace of Spades being in the top twelve: {likelihood:.2f}%")
        
        expected_avg = 100 * 12 / 52
        print(f"Expected avg: {expected_avg:.4f}%")


    class Card:
        def __init__(self, suit, value):
            self.suit = suit
            self.value = value
        
        def __eq__(self, other):
                return self.value == other.value and self.suit == other.suit
        
        def __hash__(self):
            return hash((self.value, self.suit))
        
        def __str__(self):
            value_map = {
                Numbers.TWO: '2', Numbers.THREE: '3', Numbers.FOUR: '4',
                Numbers.FIVE: '5', Numbers.SIX: '6', Numbers.SEVEN: '7',
                Numbers.EIGHT: '8', Numbers.NINE: '9', Numbers.TEN: '10',
                Numbers.JACK: 'J', Numbers.QUEEN: 'Q', Numbers.KING: 'K',
                Numbers.ACE: 'A'
            }
            return f"{value_map[self.value.value]}{self.suit.value}"
        
        def __repr__(self):
            return self.__str__()
            
        def __lt__(self, other):
            return self.value < other.value
        
if __name__ == '__main__':
    print("Running a file not intended to be run directly")