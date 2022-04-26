import lib_path
import game_engine as ge
import abstract_agent
import deck
import static_agents as sa

g = ge.Game(log_turn=False)
player1 = sa.TestPlayer("1")
player2 = sa.TestPlayer("2")
g.add_players(player1, player2)
g.deal_cards()
g.run_game()
