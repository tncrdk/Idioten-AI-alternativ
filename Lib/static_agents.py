from random import randint
import abstract_agent
import deck


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
        output = self.choose_card(playable_cards, True)
        if output != None:
            self.output = (output, None, True)
        else:
            self.output = ("n", None, True)

    def choose_card(self, playable_cards, must_play) -> int:
        cards_sorted = sorted([(card, index) for index, card in playable_cards])
        if must_play:
            for card, index in cards_sorted:
                if card.value not in {2, 10}:
                    return index
            return cards_sorted[0][1]

        for card, index in cards_sorted:
            if card.value not in {2, 10}:
                return index

        if len(cards_sorted) > 1:
            return cards_sorted[0][1]


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
    a = RandomPlayer()
    a.process_state(data)
    print(a.return_output())
