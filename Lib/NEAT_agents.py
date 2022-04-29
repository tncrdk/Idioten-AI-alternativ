from random import randint
import abstract_agent
import deck
import copy
import game_engine as ge
import neat

""" 
state_data = {
            "player": self.player,
            "playable_cards": playable_cards,
            "pile": self.pile,
            "deck": self.deck,
            "burnt_cards": self.burnt_cards,
        }
"""


class AbstractNEAT_Agent(abstract_agent.AbstractAgent):
    def __init__(self, genome, network, name="NEAT_Agent") -> None:
        super().__init__(name=name)
        self.genome = genome
        self.network = network
        self.genome.fitness = 0
        self.wrongs = 0

    def get_fitness(self):
        return self.genome.fitness

    def add_reward(self, reward: int) -> None:
        self.genome.fitness += reward


class NEAT_Agent(AbstractNEAT_Agent):
    def __init__(self, genome, network, name="NEAT_Agent") -> None:
        super().__init__(genome, network, name)

    def process_state(self, current_state_data: dict) -> None:
        future_states = []
        # [(state_data, cards_played), ... ] hvor cards_played: [(index, card), ... ]
        current_state = (current_state_data, [])
        self.find_all_next_states(current_state, future_states)
        best_state = self.get_best_state(future_states)
        # print(type(best_state))
        # self.print_state(best_state)

        # state: (state_data, cards_played)
        _, self.output = best_state

    def get_best_state(self, future_states) -> tuple:
        best_state = None
        best_state_value = -100
        for state in future_states:
            network_input = self.format_network_input(state)
            state_value = self.network.activate(network_input)[0]
            # print(state_value)
            # state_value = randint(0, 10)
            if state_value > best_state_value:
                best_state = state
                best_state_value = state_value

        # if type(best_state) == type(None):
        #     print("HALLLLLO\n\n")
        #     self.print_states(future_states)

        return best_state

    def format_network_input(self, state) -> list:
        # state: [state_data, cards_played]
        state_data, _ = state

        player = state_data.get("player")
        hand = player.hand
        table_cards = player.visible_table_cards
        opponents_cards = player.opponents_cards
        num_hidden_cards = len(player.hidden_table_cards)

        pile = state_data.get("pile")
        burnt_cards = state_data.get("burnt_cards")
        top_card_value = 0 if not pile else pile.return_top_card().value

        formatted_hand = [0 for _ in range(13)]
        formatted_table = [0 for _ in range(13)]
        formatted_opponent = [0 for _ in range(13)]
        formatted_pile = [0 for _ in range(13)]
        formatted_burnt = [0 for _ in range(13)]

        for card in hand:
            formatted_hand[card.value - 2] += 1

        for card in table_cards:
            formatted_table[card.value - 2] += 1

        for card in opponents_cards:
            formatted_opponent[card.value - 2] += 1

        for card in pile:
            formatted_pile[card.value - 2] += 1

        for card in burnt_cards:
            formatted_burnt[card.value - 2] += 1

        formatted_data = (
            formatted_hand
            + formatted_table
            + formatted_opponent
            + formatted_pile
            + formatted_burnt
        )
        formatted_data = [self.transform_input(value) for value in formatted_data]
        formatted_top_pile_card = self.transform_card_value(top_card_value)
        formatted_num_hidden = self.transform_num_hidden_card(num_hidden_cards)
        formatted_data += [formatted_top_pile_card, formatted_num_hidden]
        return formatted_data

    def transform_input(self, data):
        # range = [0,4] -> [-1, 1]
        return data / 2 - 1

    def transform_card_value(self, card_value):
        # range = [0, 12] -> [-1, 1]
        return card_value / 6 - 1

    def transform_num_hidden_card(self, num_hidden_cards):
        # range = [1, 3] -> [-1, 1]
        return num_hidden_cards - 2

    """
    STATE-SEARCHING
    """

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

    def find_immidiate_next_states(self, root_state: tuple):
        possible_next_states = []
        states_to_investigate = []
        root_state_data, cards_played = root_state
        playable_cards = root_state_data.get("playable_cards")

        for index, card in playable_cards:
            new_possible_state, new_state_to_investigate = ge.Game.simulate_play(
                index, card, root_state_data, cards_played
            )
            possible_next_states += new_possible_state
            states_to_investigate += new_state_to_investigate

        return possible_next_states, states_to_investigate

    def print_state(self, state):
        state_data, cards_played = state
        print("-" * 10)
        print("Player: ")
        for card in state_data.get("player").hand:
            card.show_card()

        print("*" * 5 + "\nCard(s) played")
        for _, card in cards_played:
            card.show_card()

    def print_states(self, states):
        for state in states:
            self.print_state(state)


""" 
state_data = {
            "player": self.player,
            "playable_cards": playable_cards,
            "pile": self.pile,
            "deck": self.deck
            "burnt_cards": self.burnt_cards,
        }
        
cards_played[(index, card), (index, card) ... ]

formatted data: ?
[0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0 ... ,antall_skjulte_kort, topp_kort]
            Hånd                        Bordet
ett kort -> 1
to kort -> 2


[0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0 ... ,antall_skjulte_kort, topp_kort]
            Kløver                      Spar

hånd_ikke_spillbare: 6
hånd_spillbare: 7
bordet: 5
haugen: 
motstander
ut_av_spill
ukjent: -1

identity activation function
"""
