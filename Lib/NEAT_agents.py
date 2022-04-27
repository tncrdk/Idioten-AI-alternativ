import abstract_agent
import deck
import copy
import game_engine as ge

""" 
state_data = {
            "player": self.player,
            "playable_cards": playable_cards,
            "pile": self.pile,
            "deck": self.deck,
            "burnt_cards": self.burnt_cards,
        }
"""


class NEAT_Agent1(abstract_agent.AbstractAgent):
    def __init__(self, name="Agent") -> None:
        super().__init__(name)

    def process_state(self, current_state_data: dict) -> None:
        future_states = []
        # [(state_data, cards_played), ... ] hvor cards_played: [(index, card), ... ]
        current_state = (current_state_data, [])
        self.find_all_next_states(current_state, future_states)
        return future_states
        # plugg inn i AI

    def find_all_next_states(self, root_state: tuple, future_states: list):
        """
        Oppdaterer future_states: [(state_data, cards_played), ... ]
        cards_played: [(index, card), ... ]
        """
        immidiate_next_states, states_to_investigate = self.find_immidiate_next_states(
            root_state
        )
        future_states += immidiate_next_states

        for state in states_to_investigate:
            self.find_all_next_states(state, future_states)

    def find_immidiate_next_states(self, root: tuple):
        possible_next_states = []
        states_to_investigate = []
        root_state_data = root[0]
        cards_played = root[1]
        playable_cards = root_state_data.get("playable_cards")

        for index, card in playable_cards:
            new_possible_state, new_state_to_investigate = ge.Game.simulate_play(
                index, card, root_state_data, cards_played
            )
            possible_next_states += new_possible_state
            states_to_investigate += new_state_to_investigate

        return possible_next_states, states_to_investigate


""" 
state_data = {
            "player": self.player,
            "playable_cards": playable_cards,
            "pile": self.pile,
            "deck": self.deck
            "burnt_cards": self.burnt_cards,
        }
        
cards_played[(index, card), (index, card) ... ]
"""
