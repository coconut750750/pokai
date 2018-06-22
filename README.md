# PokAI #
[![Build Status](https://travis-ci.org/coconut750750/pokai.svg?branch=master)](https://travis-ci.org/coconut750750/pokai)

## Overview ##
PokAI is an AI system designed in Python 3 to play the Chinese game Landlord (Dou Dizhu), a game similar to Big 2 except with a few extra types of playable hands. 

## Engine ##
The AI engine uses Monte Carlo simulations (so far). The Monte Carlo simulations tell the AI the possibility of the AI winning given a certain hand. 

To pick the best play from a list of legal plays, the AI runs a set of simulations that start off with each legal play and calculates its change of ultimately winning in the end. The AI will choose the play that optimizes the possibility of winning. 

The Monte Carlo simulations, uses three instances of ordinary Player objects with a fixed play strategy to limit confounding variables that exist when determining play strength.

## Usage ##

#### AI Versus Player Performance: ####
`ai_simulations.py` compares the performance between the AI and an ordinary player with a fixed strategy. To run the simulation:
```bash
python3 ai_simulations.py {x}
```
where {x} is strength of the starting hand.

Performance is scored based the number of wins. The AI player performs better than the fixed-strategy player by as low as 50% to as high as 400%. 

#### Real Time: ####
Before using, you must list the cards that are taken by other players so that the AI can determine the cards in its hand. List out the cards in a `.txt` file called `p{i}_cards.txt` for player i.
```bash
python3 main.py
```
To populate `p{i}_cards.txt` with random card strings run
```python3 generate_random_hands.py ```

## Building ##
Coming soon!

## Testing ##
This package uses Pytest for Unit Testing. Install it through Pip. Then, inside the root folder, run:

```bash
pytest
```

## Future Work ##
* Explore the potentials of a genetic algorithm to optimize the AI.
* Identify patterns to opponent's behaviors.
