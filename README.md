# Self-Play Game Agent

## Project Overview

Train an agent to play games through reinforcement learning and
self-play rather than relying on a labelled dataset.

The project will investigate whether an agent can develop a competent
strategy through repeated interaction with the game environment.

Games will be: Tic Tac Toe, Connect-4, Chess.

## Goals

-   Implement a reliable game environment.
-   Establish simple non-learning opponents.
-   Train a reinforcement-learning agent.
-   Investigate self-play.
-   Evaluate agents against fixed opponents and previous versions.
-   Measure training stability and performance.
-   Use the GPU effectively during training.
-   Provide a simple interface for human-vs-agent play.

## Planned Approach

### 1. Environment

Implement:

-   Board representations.
-   Legal actions.
-   State transitions.
-   Terminal-state detection.
-   Reward structure.
-   Efficient batch/environment interaction.

### 2. Baseline Opponents

Start with:

-   Random player.
-   Simple heuristic player.
-   Minimax player where practical.

These provide meaningful reference points for evaluating the learned
agent.

### 3. Reinforcement Learning

Start with a relatively simple method such as DQN or PPO.

Then investigate a stronger self-play approach:

``` text
Current agent
      ↓
Self-play
      ↓
Game trajectories
      ↓
Training data
      ↓
Policy / value network
      ↓
Updated agent
      ↓
Self-play
```

A later extension could combine policy/value learning with Monte Carlo
Tree Search.

### 4. Evaluation

Track:

-   Win rate.
-   Draw rate.
-   Average return.
-   Performance against fixed opponents.
-   Performance against previous model versions.
-   Training stability.
-   Inference latency.

Potentially maintain an Elo-style rating system for agents.

### 5. Human Interface

Provide a simple way to play:

``` text
Human
  ↓
Games interface
  ↓
Trained agent
```

This could be a small web or desktop interface.

## Good Practices

-   Keep the environment deterministic where appropriate for testing.
-   Unit-test legal moves and terminal-state detection.
-   Separate environment, agent, training and evaluation code.
-   Evaluate against fixed opponents that are not changing during
    training.
-   Use independent evaluation games rather than training games.
-   Record random seeds and training configurations.
-   Save model checkpoints.
-   Monitor training instability.
-   Avoid judging progress from a single game.
-   Evaluate multiple random seeds where practical.
-   Keep visualisation and game UI separate from the training
    implementation.

## Success Criteria

The project is successful when:

1.  The environment passes comprehensive tests.
2.  A baseline RL agent can learn non-trivial behaviour.
3.  Self-play produces measurable improvement.
4.  The final agent consistently beats simple baseline opponents.
5.  Training and evaluation are reproducible.
6.  A user can play against the trained agent.

## Possible Extensions

-   AlphaZero-style policy/value training.
-   Monte Carlo Tree Search.
-   Curriculum learning.
-   Population-based self-play.
-   Model-vs-model tournaments.
-   GPU-optimised parallel environments.

## Local CI checks

With Poetry and GNU Make available on your PATH, run these commands from the
project root:

```text
make install
make ci
```

`make ci` runs the same checks as `.github/workflows/ci.yml`: Ruff lint,
Ruff format verification, mypy, and pytest. Checks run sequentially and stop
on the first failure. Dependencies only need reinstalling when they change.
Running `make` without a target also runs the CI checks.

Individual checks are available as `make lint`, `make format-check`,
`make typecheck`, and `make test`. Use `make format` to apply formatting.

On Windows, these commands require GNU Make (not Microsoft's `nmake`).
The checks use your Poetry environment; GitHub Actions currently uses Python
3.11 on Ubuntu, so using Python 3.11 locally gives a closer match.
