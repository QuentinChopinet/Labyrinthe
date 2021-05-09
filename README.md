# Labyrinthe

This is to understand the basic of artificial neural networks.

## Description

This program use a labyrinth in a graphical interface. The labyrinth is made out of tiles :
- Purple : start
- Yellow : middle
- Green : end

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

## Installation

- Python 3.8
- Pygame

## Usage

    $python3 Labyrinth.py
