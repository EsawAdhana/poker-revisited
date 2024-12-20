
class Player:
    def __init__(self, name):
        self.name = name
        self.stack_size = 0
        self.hole_cards = set()
    
    def __str__(self):
        hole_cards = ", ".join(str(card) for card in self.hole_cards)
        result = "\n".join([
            f"Name: {self.name}",
            f"Stack Size: {self.stack_size}",
            f"Hole Cards: {hole_cards}"
        ])
        return result





'''
    Pre-flop:
        Small blind posts blind, big blind posts blind, UTG is first to act
        Action goes back to big blind, who ultimately has final option to call (if applicable), check, or raise

    Post-flop:
        Small blind is first to act
        Action goes back to button, who ultimately has final option to call (if applicable), check, or raise
    
        
Things to watch out for:
    Side pots:
        If someone goes all-in, make sure that a side pot is created equal to current size of pot + # players who call * all-in size
    Reraise/betting amounts:
        I think its 2x the big blind? But this can easily be editted later on
    

'''

if __name__ == '__main__':
    print("Running a file not intended to be run directly")