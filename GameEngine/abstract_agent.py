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

        self.hand = deck.Deck(generate_deck=False)
        self.visible_table_cards = deck.Deck(generate_deck=False)
        self.hidden_table_cards = deck.Deck(generate_deck=False)

        self.output = "no play"  # SKal være indeksen til kortet som skal spilles

    def check_if_finished(self):
        if not (self.hand or self.visible_table_cards or self.hidden_table_cards):
            self.finished = True
        return self.finished

    def sort_hand(self):
        self.hand.cards.sort()

    def process_state(self, data: dict) -> None:
        """Choose best play according to the policy"""
        pass

    def return_output(self) -> int:
        return self.output
