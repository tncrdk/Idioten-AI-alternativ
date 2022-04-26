import lib_path
import game_engine as ge
import NEAT_agents as na
import deck as ge_deck


def print_state(state):
    state_data = state[0]
    cards_played = state[1]
    print("-" * 10)
    print("Player: ")
    for card in state_data["player"].hand:
        card.show_card()

    print("*" * 5 + "\nHistory")
    for _, card in cards_played:
        card.show_card()


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
    "player": player,
    "playable_cards": ge.Game.get_playable_cards(player, pile, False),
    "pile": pile,
    "deck": deck,
    "burnt_cards": burnt_cards,
}

states = player.process_state(state)


for state in states:
    print_state(state)
