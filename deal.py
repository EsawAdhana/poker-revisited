import calculate

def deal_hole_cards(live_deck, players):
    for player in players:
        player.hole_cards.add(live_deck.pop())
    for player in players:
        player.hole_cards.add(live_deck.pop())

def deal_flop(live_deck):
    if len(live_deck) < 8:
        raise Exception(f"Missing cards. live_deck contains {len(live_deck)} cards.")
    live_deck.pop()
    flop = set()
    flop.add(live_deck.pop())
    flop.add(live_deck.pop())
    flop.add(live_deck.pop())
    return flop

def deal_turn(live_deck):
    if len(live_deck) < 4:
        raise Exception(f"Missing cards. live_deck contains {len(live_deck)} cards.")
    live_deck.pop()
    turn = set()
    turn.add(live_deck.pop())
    return turn    

def deal_river(live_deck):
    if len(live_deck) < 2:
        raise Exception(f"Missing cards. live_deck contains {len(live_deck)} cards.")
    live_deck.pop()
    river = set()
    river.add(live_deck.pop())
    return river
    
if __name__ == '__main__':
    print("Running a file not intended to be run directly")
