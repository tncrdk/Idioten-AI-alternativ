import lib_path
import neat
import game_engine as ge
import static_agents as sa
import NEAT_agents as na
import deck
import abstract_agent
import pickle


class NeatTraining:
    def __init__(
        self,
        config_path: str,
    ) -> None:
        self.config = self.load_config(config_path)

        self.population = neat.Population(self.config)
        self.population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.population.add_reporter(stats)

        self.tot_games_played = 0
        self.tot_rounds_played = 0

    def load_config(self, config_path: str):
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path,
        )
        return config

    def train_AI(self, winner_file_path: str):
        winner = self.population.run(self.eval_genomes)

        self.save_agent(winner_file_path, winner)

    def eval_genomes(self, genomes, config):
        GAMES_TO_PLAY = 100
        current_best_fitness = 0
        target_agent = sa.PlayLowSaving1("PlayLowSaving")

        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            neat_agent = na.NEAT_Agent(genome, network)

            neat_win_rate, avg_rounds_played = self.play_games(
                GAMES_TO_PLAY, neat_agent, target_agent
            )

            if neat_win_rate >= 0.4:
                neat_win_rate, avg_rounds_played = self.play_games(
                    GAMES_TO_PLAY * 10, neat_agent, target_agent
                )
            if neat_win_rate >= 0.5:
                neat_win_rate, avg_rounds_played = self.play_games(
                    GAMES_TO_PLAY * 10, neat_agent, target_agent
                )

            if avg_rounds_played <= 80:
                neat_agent.add_reward(neat_win_rate * 100)
            else:
                neat_agent.add_reward(
                    (neat_win_rate * 100) - (avg_rounds_played) * 3 + 15
                )

            agent_fitness = neat_agent.get_fitness()
            print("-" * 10)
            print(neat_win_rate)
            print(avg_rounds_played)
            print(agent_fitness)

            if agent_fitness > current_best_fitness:
                current_best_fitness = agent_fitness
                self.save_agent(r"Winners\temp_winner", genome)

    def play_games(
        self,
        games_to_play: int,
        neat_agent: abstract_agent.AbstractAgent,
        target_agent: abstract_agent.AbstractAgent,
    ) -> tuple:
        self.tot_games_played += games_to_play
        player1, player2 = neat_agent, target_agent

        for _ in range(games_to_play):
            game = ge.Game(log_game=False)
            game.add_players(player1, player2)
            game.deal_cards()

            winner, rounds_played = game.run_game()
            self.tot_rounds_played += rounds_played
            player1, player2 = player2, player1

            if winner and winner == neat_agent:
                neat_agent.wins += 1

        neat_win_rate, avg_rounds_played = self.calculate_stats(neat_agent)

        return neat_win_rate, avg_rounds_played

    def calculate_stats(self, agent: abstract_agent.AbstractAgent):
        neat_win_rate = self.calculate_win_rate(agent)
        avg_rounds_played = self.calculate_avg_rounds_played()
        return neat_win_rate, avg_rounds_played

    def calculate_win_rate(self, agent: abstract_agent.AbstractAgent):
        return agent.wins / self.tot_games_played

    def calculate_avg_rounds_played(self):
        return self.tot_rounds_played / self.tot_games_played

    def save_agent(self, save_file_path, agent_data):
        with open(save_file_path, "wb") as f:
            pickle.dump(agent_data, f)
            f.close()
