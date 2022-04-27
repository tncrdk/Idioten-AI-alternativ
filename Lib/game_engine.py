import copy
import deck
import abstract_agent


class Game:
    def __init__(self, log_game: bool, custom_deck=None) -> None:
        if bool(custom_deck):
            self.deck = custom_deck
        else:
            self.deck = deck.Deck()
        self.pile = deck.Deck(generate_deck=False)
        self.turns = 0
        self.max_rounds = 10_000
        self.burnt_cards = []
        self.log_game = log_game

    """ 
    SETUP
    """

    def add_players(
        self,
        player1: abstract_agent.AbstractAgent,
        player2: abstract_agent.AbstractAgent,
    ):
        self.players = (player1, player2)

    def deal_cards(self):
        for player in self.players:
            for _ in range(3):
                player.add_card_to_hand(self.deck.pop_top_card())
                player.visible_table_cards.add_card(self.deck.pop_top_card())
                player.hidden_table_cards.add_card(self.deck.pop_top_card())
        self.pile.add_card(self.deck.pop_top_card())

    """ 
    RUN GAME
    """

    def run_game(self):
        game_finished = False
        player, opponent = self.players[0], self.players[1]
        winner = None

        while not game_finished:
            self.turns += 1
            if player.finished:
                winner = player
                game_finished = True
                break

            self.take_turn(player, opponent)
            player, opponent = opponent, player
            game_finished = self.turns > self.max_rounds

        tot_rounds = self.turns / 2
        return winner, tot_rounds  # kan legge til flere stats kanskje

    """ 
    PLAY TURN
    """

    def take_turn(
        self,
        player: abstract_agent.AbstractAgent,
        opponent: abstract_agent.AbstractAgent,
    ):
        playable_cards = self.get_playable_cards(player, self.pile, False)
        can_play = bool(playable_cards)
        state_data = {
            "player": player,
            "playable_cards": playable_cards,
            "pile": self.pile,
            "deck": self.deck,
            "burnt_cards": self.burnt_cards,
        }

        if not can_play:
            self.can_not_play_actions(player, opponent, self.pile)

        else:
            player.process_state(state_data)
            player_input = player.return_output()
            self.make_play(
                player, opponent, player_input, self.pile, self.deck, self.burnt_cards
            )
            self.restore_player_hand(player, self.deck)
            if (
                not (self.deck or player.hand or player.visible_table_cards)
                and player.hidden_table_cards
            ):
                player.take_hidden_table_cards()
            player.check_if_finished()

        if self.log_game:
            self.log_turn(state_data, player_input)

    @classmethod
    def simulate_play(
        cls,
        index: int,
        card: deck.Card,
        root_state_data_old: dict,
        cards_played_old: list,
    ) -> tuple:
        """Simulates a play and returns ([possible_state], [state_to_investigate])"""
        root_state_data = copy.deepcopy(root_state_data_old)
        cards_played = copy.deepcopy(cards_played_old)

        player = root_state_data.get("player")
        pile = root_state_data.get("pile")
        deck = root_state_data.get("deck")
        burnt_cards = root_state_data.get("burnt_cards")
        cards_played.append((index, card))

        pile.add_card(player.play_card_by_index(index))
        cls.apply_side_effects(player, card, pile, deck, burnt_cards)

        playable_cards = cls.get_playable_cards(player, pile, is_building=True)
        new_state_data = {
            "player": player,
            "playable_cards": playable_cards,
            "pile": pile,
            "deck": deck,
            "burnt_cards": burnt_cards,
        }

        new_state = (new_state_data, cards_played)

        if (
            card.value == 10
            or card.value == 2
            or cls.check_4_in_a_row(pile)
            and player.hand
        ):
            return ([], [new_state])  # (Future_state?, state_to_investigate?)
        elif not playable_cards:
            return ([new_state], [])
        return ([new_state], [new_state])

    """ 
    ACTIONS
    """

    @classmethod
    def make_play(
        cls,
        player: abstract_agent.AbstractAgent,
        opponent: abstract_agent.AbstractAgent,
        player_input: list,  # [(index, card_played), (index, card_played), ... ]
        pile: deck.Deck,
        deck: deck.Deck,
        burnt_cards: list,
    ) -> None:
        for index, card in player_input:
            pile.add_card(player.play_card_by_index(index))
            cls.apply_side_effects(player, card, pile, deck, burnt_cards, opponent)

            if card in opponent.opponents_cards:
                opponent.opponents_cards.remove(card)

    @classmethod
    def can_not_play_actions(
        cls,
        player: abstract_agent.AbstractAgent,
        opponent: abstract_agent.AbstractAgent,
        pile: deck.Deck,
    ) -> None:
        player.hand += pile
        opponent.opponents_cards += pile.cards
        pile.clear_deck()

    @classmethod
    def restore_player_hand(
        cls, player: abstract_agent.AbstractAgent, deck: deck.Deck
    ) -> None:
        while len(player.hand) < 3 and deck:
            player.add_card_to_hand(deck.pop_top_card())

    @classmethod
    def apply_side_effects(
        cls,
        player: abstract_agent.AbstractAgent,
        card_played: deck.Card,
        pile: deck.Deck,
        deck: deck.Deck,
        burnt_cards: list,
        opponent=None,
    ) -> None:
        """Sjekker om det skal skje noe spesielt på grunn kortet som ble spilt. Hvis ja, gjennomfør disse effektene"""

        if card_played.value == 10 or cls.check_4_in_a_row(pile):
            burnt_cards += pile
            pile.clear_deck()

        if not (deck or player.hand) and player.visible_table_cards:
            if opponent:
                opponent.opponents_cards += player.visible_table_cards.cards
            player.take_visible_table_cards()

    def log_turn(self) -> None:
        pass

    """ 
    GET-FUNCTIONS
    """

    @classmethod
    def get_playable_cards(
        cls, player: abstract_agent.AbstractAgent, pile: deck.Deck, is_building: bool
    ) -> list:
        if not pile:
            playable_cards = list(enumerate(player.hand))
            return playable_cards
        playable_cards = []
        top_pile_card = pile.return_top_card()
        if is_building:
            for index, card in enumerate(player.hand):
                if cls.check_if_buildable_card(card, top_pile_card):
                    playable_cards.append((index, card))
            return playable_cards
        else:
            for index, card in enumerate(player.hand):
                if cls.check_if_playable_card(card, top_pile_card):
                    playable_cards.append((index, card))
            return playable_cards

    """
    CHECKS
    """

    @classmethod
    def check_if_playable_card(cls, card, top_pile_card) -> bool:
        if card.value == 2 or card.value == 10:
            return True
        elif card.value >= top_pile_card.value:
            return True
        return False

    @classmethod
    def check_if_buildable_card(cls, card, top_pile_card) -> bool:
        if card.value == 10:
            return False
        if top_pile_card.value == card.value:
            return True
        if top_pile_card.value + 1 == card.value:
            return True
        return False

    @classmethod
    def check_4_in_a_row(cls, pile) -> bool:
        CARDS_TO_CHECK = 4
        if len(pile) < CARDS_TO_CHECK:
            return False
        for card in pile[-CARDS_TO_CHECK + 1 :]:
            if card.value != pile[-CARDS_TO_CHECK].value:
                return False
        return True
