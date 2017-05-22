## Run an experiment with our Augmented AStar agent

First, start two instances of the Malmo Client. Then run:

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

Below is a video of our agent playing with the `FocusedAgent` collaborator, as seen from a top-down view:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=lZ4elqLYdV0
" target="_blank"><img src="http://img.youtube.com/vi/lZ4elqLYdV0/0.jpg" 
alt="Minecraft Collaborative AI challenge entry" width="480" height="360" border="10" /></a>

Below is the Reward per Episode achieved by the Augmented AStar agent:

![Performance of the Augmented AStar agent](perf.png?raw=true "Performance of the Augmented AStar agent")

## Evaluate our agent

You can evaluate our agent by running:

```
python pig_chase_eval.py
```
Results will be written to `pig_chase_results.json`.

Our results are also submitted to the leaderboard and are as follows:

Eval Score @ 100k: 1.752 | Eval Score @ 500k: 2.113
