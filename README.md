# Pythello

A Python implementation of Othello (Reversi) with a set of interchangeable AI
opponents, built to compare game-playing strategies on the same board engine.

## Players

- Random and random-learning baselines
- Heuristic (positional weighting)
- Minimax, plus an optimized minimax with alpha-beta pruning
- Monte Carlo Tree Search (MCTS)

## Stack

- Python 3. See `requirements.txt` (pytest for the test suite).

## Run

```bash
python runner.py        # play a game between two configured players
pytest                  # run the test suite
```

Swap the players constructed in `runner.py` to pit any two strategies against
each other.

## Structure

- `game/` — board, points, and rules.
- `players/` — one module per strategy.
- `tests/` — board, player, and runner tests.

See [IMPROVEMENTS.md](IMPROVEMENTS.md) for the bug-fix and optimization notes.

## License

MIT — see [LICENSE](LICENSE).
