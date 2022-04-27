import lib_path
import game_engine as ge
import NEAT_agents as na
import static_agents as sa
import deck as ge_deck


def print_state(state):
    state_data = state[0]
    cards_played = state[1]
    print("-" * 10)
    print("Player: ")
    for card in state_data.get("player").hand:
        card.show_card()

    print("*" * 5 + "\nCard(s) played")
    for _, card in cards_played:
        card.show_card()


def print_moves(moves):
    i = 1
    for index, card in moves:
        print("-" * 10 + f"\n{i}")
        print(f"Index: {index}")
        card.show_card()
        i += 1


NINE_OF_CLUBS = ge_deck.Card(9, ge_deck.Card.SUITS.CLUBS)

JACK_OF_HEARTS = ge_deck.Card(11, ge_deck.Card.SUITS.HEARTS)
JACK_OF_CLUBS = ge_deck.Card(11, ge_deck.Card.SUITS.CLUBS)
JACK_OF_DIAMOND = ge_deck.Card(11, ge_deck.Card.SUITS.DIAMONDS)
JACK_OF_SPADES = ge_deck.Card(11, ge_deck.Card.SUITS.SPADES)

QUEEN_OF_SPADES = ge_deck.Card(12, ge_deck.Card.SUITS.SPADES)
QUEEN_OF_HEARTS = ge_deck.Card(12, ge_deck.Card.SUITS.HEARTS)
ACE_OF_SPADES = ge_deck.Card(14, ge_deck.Card.SUITS.SPADES)

THREE_OF_SPADES = ge_deck.Card(3, ge_deck.Card.SUITS.SPADES)
THREE_OF_HEARTS = ge_deck.Card(3, ge_deck.Card.SUITS.HEARTS)
THREE_OF_DIAMONDS = ge_deck.Card(3, ge_deck.Card.SUITS.DIAMONDS)

FOUR_OF_SPADES = ge_deck.Card(4, ge_deck.Card.SUITS.SPADES)
FOUR_OF_HEARTS = ge_deck.Card(4, ge_deck.Card.SUITS.HEARTS)
FOUR_OF_DIAMONDS = ge_deck.Card(4, ge_deck.Card.SUITS.DIAMONDS)
FOUR_OF_CLUBS = ge_deck.Card(4, ge_deck.Card.SUITS.CLUBS)


pile = ge_deck.Deck(generate_deck=False)
pile.add_card(NINE_OF_CLUBS)
deck = ge_deck.Deck()
burnt_cards = []

# player = na.NEAT_Agent1()
player = sa.PlayLowSaving1()

player.hand.cards += [
    QUEEN_OF_HEARTS,
    QUEEN_OF_SPADES,
    ACE_OF_SPADES,
    FOUR_OF_CLUBS,
    JACK_OF_CLUBS,
    JACK_OF_DIAMOND,
    JACK_OF_HEARTS,
    JACK_OF_SPADES,
]
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
    "playable_cards": ge.Game.get_playable_cards(player, pile, is_building=False),
    "pile": pile,
    "deck": deck,
    "burnt_cards": burnt_cards,
}

# states = player.process_state(state)
# for state in states:
#     print_state(state)

player.process_state(state)
moves = player.return_output()
print_moves(moves)
