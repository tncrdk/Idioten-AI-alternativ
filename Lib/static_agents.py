from random import randint
from tkinter import N
from black import out

from numpy import choose
import abstract_agent
import deck
import game_engine as ge


class PlayLow_NoBuilding(abstract_agent.AbstractAgent):
    def __init__(self, name="Agent") -> None:
        super().__init__(name)

    def process_state(self, state_data: dict) -> None:
        playable_cards = state_data.get("playable_cards")
        index, card = self.get_smallest_card(playable_cards)
        self.output = [(index, card)]

    def get_smallest_card(self, playable_cards) -> int:
        smallest_card = 15
        for i, card in playable_cards:
            if card.value < smallest_card:
                smallest_card = card
                smallest_card_index = i

        return smallest_card_index, smallest_card


# TODO Må fikses på
class PlayLowSaving_NoBuilding(abstract_agent.AbstractAgent):
    def __init__(self, name="Agent") -> None:
        super().__init__(name)

    def process_state(self, state_data: dict) -> None:
        playable_cards = state_data.get("playable_cards")
        index, card = self.choose_card(playable_cards, True)
        self.output = [(index, card)]

    def choose_card(self, playable_cards, must_play) -> int:
        cards_sorted = sorted([(card, index) for index, card in playable_cards])
        if must_play:
            for card, index in cards_sorted:
                if card.value not in {2, 10}:
                    return index, card
            return cards_sorted[0]

        for card, index in cards_sorted:
            if card.value not in {2, 10}:
                return index, card

        if len(cards_sorted) > 1:
            return cards_sorted[0]


class PlayLowSaving1(abstract_agent.AbstractAgent):
    def __init__(self, name="Agent") -> None:
        super().__init__(name)

    def process_state(self, state_data: dict) -> None:
        cards_played = []
        self.output = self.choose_cards(state_data, cards_played, must_play=True)

    def choose_cards(
        self, state_data: dict, cards_played: list, must_play: bool
    ) -> list:
        playable_cards = state_data.get("playable_cards")
        playable_cards.sort(key=lambda x: x[1])

        if must_play:
            index, card = playable_cards[0]
            for i, c in playable_cards:
                if c.value not in {2, 10}:
                    index, card = i, c
                    break
            cards_played = self.choose_next_cards(index, card, state_data, cards_played)
            return cards_played

        else:
            index, card = None, None
            for i, c in playable_cards:
                if c.value not in {2, 10}:
                    index, card = i, c
                    break
            if index == None:
                return cards_played
            cards_played = self.choose_next_cards(index, card, state_data, cards_played)
            return cards_played

    def get_next_state(self, index, card, state_data, cards_played):
        # next_state : [(state_data, cards_played)]
        _, next_state = ge.Game.simulate_play(index, card, state_data, cards_played)
        if next_state:
            return next_state[0]
        return None

    def choose_next_cards(self, index, card, state_data, cards_played):
        next_state = self.get_next_state(index, card, state_data, cards_played)
        if not next_state:
            cards_played.append((index, card))
            return cards_played

        next_state_data, cards_played = next_state
        cards_played = self.choose_cards(next_state_data, cards_played, False)
        return cards_played


class RandomPlayer(abstract_agent.AbstractAgent):
    def __init__(self, name="Agent") -> None:
        super().__init__(name)

    def process_state(self, state_data: dict) -> None:
        playable_cards = state_data.get("playable_cards")
        length = len(playable_cards)
        rand_index = randint(0, length - 1)
        card = playable_cards[rand_index][1]
        self.output = [(rand_index, card)]


class TestPlayer(abstract_agent.AbstractAgent):
    def __init__(self, name="Agent") -> None:
        super().__init__(name)

    def process_state(self, state_data: dict) -> None:
        playable_cards = state_data.get("playable_cards")
        index, card = playable_cards[0]
        self.output = [(index, card)]

        # self.show_play(state_data, card)


if __name__ == "__main__":
    data = {"playable_cards": [(0, 8), (1, 8), (2, 8), (3, 9), (4, 9), (5, 9)]}
    a = PlayLowSaving1()
    a.process_state(data)
    print(a.return_output())
