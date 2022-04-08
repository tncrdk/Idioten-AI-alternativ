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
        if not (self.deck or self.hand) and self.visible_table_cards:
            self.hand += self.visible_table_cards
            self.visible_table_cards.clear_deck()

    def take_hidden_table_cards(self):
        if not (self.hand or self.visible_table_cards) and self.hidden_table_cards:
            self.add_card_to_hand(self.player.table_hidden.pop())

    """
    AI
    """

    def return_output(self) -> list:
        return self.output

    def process_state(self, state: dict) -> None:
        """Choose best play according to the policy"""
        pass


class NEAT_Agent1(AbstractAgent):
    def __init__(self, name="Agent") -> None:
        super().__init__(name)

    def process_state(self, current_state: dict) -> None:
        possible_states = []  # [(card_played, state{})]
        self.find_possible_states(current_state, possible_states)

    def find_possible_states(self, root_state: dict, possible_states: list):

        next_states = []  # Next to be investigated, using root_state
        possible_states += next_states

        for state in next_states:
            self.find_possible_states(state, possible_states)
