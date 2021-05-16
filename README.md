# Labyrinthe

This is to understand the basic of artificial neural networks.

## Description

This program use a labyrinth in a graphical interface. The labyrinth is made out of tiles :
- Purple : start
- Yellow : middle
- Green : end
The board matrix is filled with :
- 0 for start tile
- 1 for empty tiles
- 2 for middle tiles
- 6 for end tile

The user can choose from mutliple labyrinth configuration.

The AI is the blue dot. Its goal is to reach the end tile. The AI can move to the adjacent up/down/right/left tile (no diagonal). If the AI get out of the tiles, it dies.
The AI dies alsow if it does more moves than the number of tiles on a square labyrinth (100 tiles).

The AI get a score when it reach the end or when it dies.

Score points are :
- +1 point per tile traveled verticaly away from the start  
- +1 point per tile traveled horizontaly away from the start
- -5 for geting out of the labyrinth (for dying)
- +number of remaning moves (100 minus move done)

The AI with the best score of the round is selected. This selected AI is duplicated with random mutation for the next round.

The AI is a neural networks based on NEAT (NeuroEvolution of Augmenting Topologies) with :
- 4 inputs (nbInput) : the number of the tiles in the 4 directions from the AI position
- 3 layers (nbCouche)
- 3 neurons by layer (nbNeuroneParCouche)
- 4 outputs neurons (nbOutput) : each has an assigned direction
- 5 AI by generation (nbIA)
- 10% of mutation per new generation (pourcentCoeffModif)
Each neuron takes one or more number between -1 and 1 in input. The output of a neuron is a number between -1 and 1. This output is the sum of the inputs by a coefficient. Each neuron has its own set of coefficient store in the AI matrix. In the end, the highest output neuron give the direction.

## Installation

- Python 3.8
- Pygame

## Usage

    $python3 Labyrinth.py
