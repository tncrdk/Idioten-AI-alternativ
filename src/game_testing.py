import lib_path
import game_engine as ge
import abstract_agent
import deck
import static_agents as sa

g = ge.Game(log_game=False)
player1 = sa.PlayLow_Nobuilding_Player("1")
player2 = sa.TestPlayer("2")
g.add_players(player1, player2)
g.deal_cards()
winner, _ = g.run_game()
if winner:
    print(winner.name)
