import enum
import deck
import abstract_agent


class Game:
    def __init__(self, custom_deck=None) -> None:
        if bool(custom_deck):
            self.deck = custom_deck
        else:
            self.deck = deck.Deck()
        self.pile = deck.Deck(generate_deck=False)

        self.turns = 0
        self.max_rounds = 10_000
        self.burnt_cards = []

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
                player.visible_table_cards.append(self.deck.pop_top_card())
                player.hidden_table_cards.append(self.deck.pop_top_card())
        self.pile.add_card(self.deck.pop_top_card())

    """ 
    RUN GAME
    """

    def run_game(self):
        game_finished = False
        player, opponent = self.players[0], self.players[1]

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

    def take_turn(self, player: abstract_agent.AbstractAgent, oppnonent):
        playable_cards = self.get_playable_cards()
        can_play = bool(playable_cards)
        state = {
            "player_hand": player.hand,
            "playable_cards": playable_cards,
            "player_visible_table_cards": player.visible_table_cards,
            "opponents_cards": player.opponents_cards,
            "pile": self.pile,
            "burnt_cards": self.burnt_cards,
        }

        if not can_play:
            self.can_not_play_actions(playable_cards, player, oppnonent)

        else:
            player.process_state(state)
            player_input = (
                player.return_output()
            )  # Returnerer en liste med hvert trekk spilleren gjør i riktig rekkefølge
            self.make_play(player_input)
            self.restore_player_hand(player)
            if not self.deck:
                player.take_visible_table_cards()

        if not self.deck:
            player.take_hidden_table_cards()
        player.check_if_finished()

    """ 
    ACTIONS
    """

    def make_play(self, player: abstract_agent.AbstractAgent, player_input: list):
        for play in player_input:
            player.play_card(play)
            self.apply_side_effects(play)
            # add to oppnents_cards

    def can_not_play_actions(
        self,
        player: abstract_agent.AbstractAgent,
        opponent: abstract_agent.AbstractAgent,
    ):
        player.hand += self.pile.cards
        opponent.opponents_cards += self.pile.cards
        self.pile.clear()

    def restore_player_hand(self, player: abstract_agent.AbstractAgent):
        while len(player.hand) < 3 and self.deck:
            player.add_card_to_hand(self.deck.pop_top_card())

    def log_turn(self):
        pass
