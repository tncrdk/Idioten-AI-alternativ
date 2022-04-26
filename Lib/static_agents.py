from random import randint

from numpy import place
import abstract_agent
import deck


class RandomPlayer(abstract_agent.AbstractAgent):
    def __init__(self, name="Agent") -> None:
        super().__init__(name)

    def process_state(self, state_data: dict) -> None:
        playable_cards = state_data["playable_cards"]
        length = len(playable_cards)
        rand_index = randint(0, length - 1)
        card = playable_cards[rand_index][1]
        self.output = [(rand_index, card)]

        print("-" * 10)
        print("Hand")
        for i in self.hand:
            i.show_card()
        print("*" * 20 + "\nPlayed card")
        card.show_card()
        print("*" * 20 + "\nPile")
        pile = state_data["pile"]
        if pile:
            pile.return_top_card().show_card()
        print("-" * 20)


class TestPlayer(abstract_agent.AbstractAgent):
    def __init__(self, name="Agent") -> None:
        super().__init__(name)

    def process_state(self, state_data: dict) -> None:
        playable_cards = state_data["playable_cards"]
        index, card = playable_cards[0]

        print("-" * 10)
        print("Pile:")
        pile = state_data["pile"]
        if pile:
            pile.return_top_card().show_card()
        print("*" * 20 + "\nHand:")
        for i in self.hand:
            i.show_card()
        print("*" * 20 + "\nPlayed card")
        card.show_card()
        print("-" * 20 + "\n\n")

        self.output = [(index, card)]


if __name__ == "__main__":
    data = {"playable_cards": [(0, 8), (1, 8), (2, 8), (3, 9), (4, 9), (5, 9)]}
    a = RandomPlayer()
    a.process_state(data)
    print(a.return_output())
