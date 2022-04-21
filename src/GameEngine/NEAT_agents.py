import GameEngine.abstract_agent as abstract_agent
import GameEngine.deck as deck
import copy
import GameEngine.game_engine as ge

""" 
state_data = {
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

    def process_state(self, current_state_data: dict) -> None:
        future_states = []  # [(state_data, cards_played[(index, card)])]
        current_state = (current_state_data, [])
        self.find_all_possible_states(current_state, future_states)
        # plugg inn i AI

    def find_all_possible_states(self, root_state: tuple, future_states: list):
        """
        Oppdaterer future_states: [(state_data, cards_played)]
        cards_played: [(index, card)]
        """
        possible_next_states, states_to_investigate = self.find_next_states(root_state)
        future_states += possible_next_states

        for state in states_to_investigate:
            self.find_all_possible_states(state, future_states)

    def find_next_states(self, root: tuple):
        possible_next_states = []
        states_to_investigate = []
        playable_cards = root[0]["playable_cards"]

        for index, card in playable_cards:
            root_state_data = copy.deepcopy(root[0])
            cards_played = copy.deepcopy(root[1])
            new_possible_state, new_state_to_investigate = ge.Game.simulate_play(
                index, card, root_state_data, cards_played
            )
            possible_next_states += new_possible_state
            states_to_investigate += new_state_to_investigate

        return possible_next_states, states_to_investigate


# cards_played[(index, card)]
""" 
state_data = {
            "player_hand": player.hand,
            "playable_cards": playable_cards,  [(index, card)]
            "player_visible_table_cards": player.visible_table_cards,
            "opponents_cards": player.opponents_cards,
            "pile": self.pile,
            "burnt_cards": self.burnt_cards,
        }
"""
