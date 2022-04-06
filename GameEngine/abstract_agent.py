import deck

"""
Format på input:

data = {
    hand_cards: [...],
    playable_cards: [...],
    table_cards: [...],
    pile: [...],
    played_cards: [...],
    burnt_cards: [...]
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

        self.output = "no play"  # Skal være indeksen til kortet som skal spilles

    """ Spiller """

    def check_if_finished(self):
        if not (self.hand or self.visible_table_cards or self.hidden_table_cards):
            self.finished = True
        return self.finished

    def sort_hand(self):
        self.hand.cards.sort()

    def add_card_to_hand(self, card: deck.Card):
        self.hand.add_card(card)

    def take_visible_table_cards(self):
        pass

    def take_hidden_table_cards(self):
        pass

    """ AI """

    def process_state(self, data: dict) -> None:
        """Choose best play according to the policy"""
        pass

    def return_output(self) -> int:
        return self.output
