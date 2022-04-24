import GameEngine.game_engine as ge
import GameEngine.NEAT_agents as na
import GameEngine.deck as ge_deck


THREE_OF_CLUBS = ge_deck.Card(3, ge_deck.Card.SUITS.CLUBS)

QUEEN_OF_SPADES = ge_deck.Card(12, ge_deck.Card.SUITS.SPADES)
QUEEN_OF_HEARTS = ge_deck.Card(12, ge_deck.Card.SUITS.HEARTS)
ACE_OF_SPADES = ge_deck.Card(14, ge_deck.Card.SUITS.SPADES)

THREE_OF_SPADES = ge_deck.Card(3, ge_deck.Card.SUITS.SPADES)
THREE_OF_HEARTS = ge_deck.Card(3, ge_deck.Card.SUITS.HEARTS)
THREE_OF_DIAMONDS = ge_deck.Card(3, ge_deck.Card.SUITS.DIAMONDS)

FOUR_OF_SPADES = ge_deck.Card(4, ge_deck.Card.SUITS.SPADES)
FOUR_OF_HEARTS = ge_deck.Card(4, ge_deck.Card.SUITS.HEARTS)
FOUR_OF_DIAMONDS = ge_deck.Card(4, ge_deck.Card.SUITS.DIAMONDS)


pile = ge_deck.Deck(generate_deck=False)
pile.add_card(THREE_OF_CLUBS)
deck = ge_deck.Deck()
burnt_cards = []

player = na.NEAT_Agent1()

player.hand.cards += [QUEEN_OF_HEARTS, QUEEN_OF_SPADES, ACE_OF_SPADES]
player.visible_table_cards.cards += [
    THREE_OF_DIAMONDS,
    THREE_OF_HEARTS,
    THREE_OF_SPADES,
]
player.hidden_table_cards.cards += [
    FOUR_OF_DIAMONDS,
    FOUR_OF_HEARTS,
    FOUR_OF_SPADES,
]

state = {
    "player_hand": player.hand,
    "playable_cards": ge.Game.get_playable_cards(player, pile, False),
    "player_visible_table_cards": player.visible_table_cards,
    "opponents_cards": player.opponents_cards,
    "pile": pile,
    "deck": deck,
    "burnt_cards": burnt_cards,
}

print("-" * 10)
for card in state["player_hand"]:
    card.show_card()
print("Pile: ")
pile.return_top_card().show_card()
print("-" * 10)

states = player.process_state(state)

print(states)
