import abstract_agent
import deck
import copy

""" 
state = {
            "player_hand": player.hand,
            "playable_cards": playable_cards,  [(index, card)]
            "player_visible_table_cards": player.visible_table_cards,
            "opponents_cards": player.opponents_cards,
            "pile": self.pile,
            "burnt_cards": self.burnt_cards,
        }
"""


class NEAT_Agent1(abstract_agent.AbstractAgent):
    def __init__(self, name="Agent") -> None:
        super().__init__(name)

    def process_state(self, current_state: dict) -> None:
        possible_states = []  # [(cards_played[(index, card)], state{})]
        root = (current_state, [])
        self.find_all_possible_states(root, possible_states)

    def find_all_possible_states(self, root: tuple, possible_states: list):
        next_states = self.find_next_states(root)
        if bool(next_states):
            possible_states += next_states
            for state in next_states:
                self.find_all_possible_states(state, possible_states)

    def find_next_states(self, root: tuple):
        next_states = []
        playable_cards = root[0]["playable_cards"]

        for index, card in playable_cards:
            root_state = copy.deepcopy(root[0])
            cards_played = copy.deepcopy(root[1])
            next_states += self.get_next_state(index, card, root_state, cards_played)

        return next_states

    def get_next_state(
        self, index: int, card: deck.Card, root_state: dict, cards_played: list
    ):
        pass
