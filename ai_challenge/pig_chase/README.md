# Malmo Collaborative AI Challenge - Pig Chase - Augmented AStar agent

This repository contains our entry for the Malmo Collaborative AI challenge task. The challenge task takes the form of a collaborative mini game, called Pig Chase.

![Screenshot of the pig chase game](pig-chase-overview.png?raw=true "Screenshot of the Pig Chase game")

## Overview of the game

Two Minecraft agents and a pig are wandering a small meadow. The agents have two choices:

- _Catch the pig_ (i.e., the agents pinch or corner the pig, and no escape path is available), and receive a high reward (25 points)
- _Give up_ and leave the pig pen through the exits to the left and right of the pen, marked by blue squares, and receive a small reward (5 points)

The pig chased is inspired by the variant of the _stag hunt_ presented in [Yoshida et al. 2008]. The [stag hunt](https://en.wikipedia.org/wiki/Stag_hunt) is a classical game theoretic game formulation that captures conflicts between collaboration and individual safety.

[Yoshida et al. 2008] Yoshida, Wako, Ray J. Dolan, and Karl J. Friston. ["Game theory of mind."](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000254) PLoS Comput Biol 4.12 (2008): e1000254.


## How to play (human players)

To familiarize yourself with the game, we recommend that you play it yourself. The following instructions allow you to play the game with a "focused agent". A baseline agent that tries to move towards the pig whenever possible. There are also instructions for playing with our Augmented AStar agent. 

### Prerequisites

* Install the [Malmo Platform](https://github.com/Microsoft/malmo) and the `malmopy` framework as described under [Installation](../../README.md#installation), and verify that you can run the Malmo platform and python example agents

### Steps

* Start two instances of the Malmo Client on ports `10000` and `10001`
* `cd malmo-challenge/ai_challenge/pig_chase`
* `python pig_chase_human_vs_agent.py`

### Playing with our agent
If you want to play with our Augmented AStar agent instead of the 'focused' baseline agent, run:
* `python pig_chase_human_vs_agent.py -t myagent`


Wait for a few seconds for the human player interface to appear.

Note: the script assumes that two Malmo clients are running on the default ports on localhost. You can specify alternative clients on the command line. See the script's usage instructions (`python pig_chase_human_vs_agent.py -h`) for details.

### How to play

* The game is played over 10 rounds at a time. Goal is to accumulate the highest score over these 10 rounds.
* In each round a "collaborator" agent is selected to play with you. Different collaborators may have different behaviors.
* Once the game has started, use the left/right arrow keys to turn, and the forward/backward keys to move. You can see your agent move in the first person view, and shown as a red arrow in the top-down rendering on the left.
* You and your collaborator move in turns and try to catch the pig (25 points if caught). You can give up on catching the pig in the current round by moving to the blue "exit squares" (5 points). You have a maximum of 25 steps available, and will get -1 point for each step taken.

## Run an experiment with our Augmented AStar agent

First, start two instances of the Malmo Client as [above](#steps). Then run:

```
python pig_chase_experiment.py -t myagent
```

Depending on whether `tensorboard` is available on your system, this script will output performance statistics to either tensorboard or to console. If using tensorboard, you can plot the stored data by pointing a tensorboard instance to the results folder:

```
cd ai_challenge/pig_chase
tensorboard --logdir=results --port=6006
```

You can also run a `RandomAgent` or `FocusedAgent` baseline. Switch agents using the command line arguments:

```
python pig_chase_experiment.py -t random
```
For additional command line options, see the usage instructions: `python pig_chase_experiment.py -h`.

You can then navigate to http://127.0.0.1:6006 to view the results.

## Description of our Augmented AStar agent

Our Augmented AStar agent entry for the Malmo Collaborative AI challenge is based off the AStar pathfinding algorithm. When choosing an action, it takes into account its own position and the position of the pig relative to itself, the position of the collaborator agent relative to itself and the pig, and the collaborator agent's behavior.

It also exploits the fact that the pig behaves as a normal Minecraft mob. If the pig is in an unfavorable position (eg. it can't be caught), it holds off making a move until the pig moves and goes to a position where it's easier to catch.

Below is a video of our agent playing with the `FocusedAgent` collaborator:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=lZ4elqLYdV0
" target="_blank"><img src="http://img.youtube.com/vi/lZ4elqLYdV0/0.jpg" 
alt="Minecraft Collaborative AI challenge entry" width="480" height="360" border="10" /></a>

## Evaluate our agent

We provide a commodity evaluator PigChaseEvaluator, which allows you to quickly evaluate
the performance of your agent.
