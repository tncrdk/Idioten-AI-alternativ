import abstract_agent
import deck
import copy
import game_engine as ge

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
        possible_states = []  # [(state{}, cards_played[(index, card)])]
        root = (current_state, [])
        self.find_all_possible_states(root, possible_states)

    def find_all_possible_states(self, root: tuple, possible_states: list):
        possible_next_states, states_to_investigate = self.find_next_states(root)
        possible_states += possible_next_states

        if bool(states_to_investigate):
            for state in states_to_investigate:
                self.find_all_possible_states(state, possible_states)

    def find_next_states(self, root: tuple):
        possible_next_states = []
        states_to_investigate = []
        playable_cards = root[0]["playable_cards"]

        for index, card in playable_cards:
            root_state = copy.deepcopy(root[0])
            cards_played = copy.deepcopy(root[1])
            sim_output = ge.Game.simulate_play(index, card, root_state, cards_played)
            possible_next_states += sim_output[0]
            states_to_investigate += sim_output[1]

        return possible_next_states, states_to_investigate


# cards_played[(index, card)]
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
