import neat_training as nt

config_path = r"Config-files\config.txt"
trainer = nt.NeatTraining(config_path)
trainer.train_AI(r"Winner\winner")
