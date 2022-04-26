from enum import Enum
import numpy.random as np_rand


class Card:
    SYMBOLS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    LOWER_VALUE_LIMIT = 2
    UPPER_VALUE_LIMIT = 14

    class SUITS(Enum):
        DIAMONDS = "diamonds"
        HEARTS = "hearts"
        SPADES = "spades"
        CLUBS = "clubs"

    def __init__(self, value: int, suit) -> None:
        if value > self.UPPER_VALUE_LIMIT or value < self.LOWER_VALUE_LIMIT:
            raise ValueError("Card value is out of bounds")
        if type(suit) != self.SUITS:
            raise ValueError("Suit is not of type SUIT")
        self.value = value
        self.suit = suit
        self.symbol = self.SYMBOLS[value - 2]

    def __gt__(self, other):
        return self.value > other

    def __lt__(self, other):
        return self.value < other

    def show_card(self) -> None:
        print(f"{self.symbol} of {self.suit.value} ({self.value})")


class Deck:
    def __init__(self, generate_deck=True) -> None:
        self.cards = []
        self.is_generated = False

        if generate_deck:
            self.generate()
            self.is_generated = True

    def __bool__(self):
        return bool(self.cards)

    def __add__(self, i):
        if type(i) != Deck:
            raise TypeError("Må være av typen 'Deck'")
        self.cards += i.cards
        return self

    def __getitem__(self, index):
        return self.cards[index]

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def shuffle(self) -> None:
        np_rand.shuffle(self.cards)

    def generate(self) -> None:
        if not self.is_generated:
            for suit in Card.SUITS:
                for value in range(Card.LOWER_VALUE_LIMIT, Card.UPPER_VALUE_LIMIT + 1):
                    self.cards.append(Card(value, suit))
            self.shuffle()
            self.is_generated = True

    def pop_top_card(self) -> Card:
        return_card = self.cards.pop()
        return return_card

    def return_top_card(self) -> Card:
        return self.cards[-1]

    def add_card(self, card) -> None:
        if type(card) == Card:
            self.cards.append(card)
        else:
            raise TypeError("Det er ikke av typen kort")

    def pop_card_by_index(self, index):
        return self.cards.pop(index)

    def pop_card_by_card(self, card):
        self.cards.remove(card)

    def clear_deck(self) -> None:
        self.cards.clear()
