import deck
import abstract_agent


class Game:
    def __init__(self, custom_deck=None) -> None:
        if bool(custom_deck):
            self.deck = custom_deck
        else:
            self.deck = deck.Deck()
        self.pile = deck.Deck(generate_deck=False)

        self.rounds = 0
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
                player.table_visible.append(self.deck.pop_top_card())
                player.table_hidden.append(self.deck.pop_top_card())
        self.pile.add_card(self.deck.pop_top_card())

    """ 
    RUN GAME
    """

    def run_game(self):
        game_finished = False

        while not game_finished:
            self.rounds += 1
            for player in self.players:
                if player.finished:
                    winner = player
                    game_finished = True
                    break
                self.take_turn(player)
            game_finished = self.rounds > self.max_rounds
        return winner, self.rounds  # kan legge til flere stats kanskje

    """ 
    PLAY TURN
    """

    def take_turn(self, player: abstract_agent.AbstractAgent):
        playable_cards = self.get_playable_cards()
        can_play = bool(playable_cards)

        if not can_play:
            self.can_not_play_actions(playable_cards)

        else:
            player.process_state()
            player_input = self.get_player_input(playable_cards)
            self.make_play(player_input)
            player.take_visible_table_cards()  # Funksjonen sjekker om spilleren har mulighet også
            self.restore_hand()

        player.take_hidden_table_cards()
        player.check_if_finished()

    def make_play(self, player_input):
        self.apply_side_effects(player_input)

    def log_turn(self):
        pass
