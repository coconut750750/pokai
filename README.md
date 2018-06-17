# PokAI #

### Overview ###
PokAI is an AI system designed in Python 3 to play the Chinese game Landlord (Dou Dizhu), a game similar to Big 2 except with a few extra types of playable hands. 

### Usage ###
Before using, you must list the cards that are taken by other players so that the AI can determine the cards in its hand. List out the cards in a `.txt` file called `p{x}_cards.txt` for player x.

```bash
python3 -m pokai.main
```

### Building ###
Coming soon!

### Testing ###
This package uses Pytest for Unit Testing. Install it through Pip. Then, inside the root folder, run:

```bash
pytest
```

### Engine ###
The AI engine uses Monte Carlo simulations and probability calculations to determine the strength of each play (so far). The Monte Carlo simulations tell the AI the possibility of the AI winning given a certain hand. 

To pick the best play from a list of legal plays, the AI runs a set of simulations for each play and chooses the play that maximizes the possibility of winning. 

The AI also takes into account the probability of an opponent having a play that can beat the AI's play. 

### Future Work ###
* Explore the potentials of a genetic algorithm to optimize the AI.
* Identify patterns to opponent's behaviors.
