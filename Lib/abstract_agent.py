import deck

"""
Format på input:

state = {
        "playable_cards": {},
        "pile": [],
        "burnt_cards": []
    }
"""


class AbstractAgent:
    def __init__(self, name="Agent") -> None:
        self.name = name
        self.finished = False
        self.opponents_cards = []

        self.hand = deck.Deck(generate_deck=False)
        self.visible_table_cards = deck.Deck(generate_deck=False)
        self.hidden_table_cards = deck.Deck(generate_deck=False)

    """ 
    PLAYER
    """

    def check_if_finished(self):
        if not (self.hand or self.visible_table_cards or self.hidden_table_cards):
            self.finished = True
        return self.finished

    def sort_hand(self):
        self.hand.cards.sort()

    def add_card_to_hand(self, card: deck.Card):
        self.hand.add_card(card)

    def take_visible_table_cards(self):
        self.hand += self.visible_table_cards
        self.visible_table_cards.clear_deck()

    def take_hidden_table_cards(self):
        self.add_card_to_hand(self.hidden_table_cards.pop_top_card())

    def play_card_by_index(self, index):
        return self.hand.pop_card_by_index(index)

    def show_play(self, state_data: dict, card_to_play: deck.Card):
        print("-" * 10)
        print("Pile:")
        pile = state_data["pile"]
        if pile:
            pile.return_top_card().show_card()
        print("*" * 20 + "\nHand:")
        for i in self.hand:
            i.show_card()
        print("*" * 20 + "\nPlayed card")
        card_to_play.show_card()
        print("-" * 20 + "\n\n")

    """
    AI
    """

    def return_output(self) -> list:
        """Returns a list with moves in correct order"""
        return self.output

    def process_state(self, state_data: dict) -> None:
        """Choose best play according to the policy"""
        pass
