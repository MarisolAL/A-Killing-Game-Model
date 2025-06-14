# A Killing Game Model

Inspired by the _Danganronpa_ series, this project simulates a simplified version of a "killing game" using Python 2 and the [Processing.py](https://py.processing.org/) framework for visualization.

The simulation models a group of players (referred to as "particles") that interact on a board and transition through multiple phases, including social bonding, murder, and investigation.

# Game Overview

The game simulates a loop of three main phases across a board populated with interacting agents.

## Phase 0: Social Interaction

Particles interact randomly, affecting affinity levels between them.

Occasionally, despair levels increase due to external incentives.

When any particle reaches maximum despair, the game transitions to Phase 1.

## Phase 1: The Killing

A player driven to despair becomes the killer.

The killer searches for a target and kills a visible neighbor.

Another nearby particle witnesses the murder.

The game immediately moves to Phase 2.

## Phase 2: Investigation

The witness tries to spread the identity of the killer to nearby particles.

Particles will believe the accusation only if their affinity with the accuser is high enough.

This phase lasts for 35 iterations.

If by the end, less than 50% of the surviving players know the correct killer: The killer wins.

Otherwise: The killer is eliminated, and the game returns to Phase 0.

# Execution

To run the simulation:

* Make sure you have Python 2 installed.

* Install and set up Processing.py.

* Run the file `main.pyde` through the Processing IDE.

## Notes

This is a conceptual simulation and uses basic agent behavior modeling.

The project was developed for experimentation and creative exploration of emergent group dynamics under simple rules.
